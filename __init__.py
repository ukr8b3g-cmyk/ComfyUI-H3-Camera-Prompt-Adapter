import math

from comfy_api.latest import ComfyExtension, io


def _camera_details(camera_info):
    try:
        if camera_info["cameraType"] != "perspective":
            return "", ""
        position = camera_info["position"]
        target = camera_info["target"]
        x, y, z = (float(position[axis]) - float(target[axis]) for axis in "xyz")
    except (KeyError, TypeError, ValueError, OverflowError):
        return "", ""

    radius = math.hypot(x, y, z)
    if not math.isfinite(radius) or not 0.599999 <= radius <= 2.600001:
        return "", ""

    horizontal = math.hypot(x, z)
    elevation = round(math.degrees(math.atan2(y, horizontal)))
    if not -30 <= elevation <= 60:
        return "", ""

    signed_azimuth = round(math.degrees(math.atan2(x, z)))
    azimuth = signed_azimuth % 360
    if azimuth == 0:
        direction = "0 degrees at the reference viewpoint"
    elif azimuth == 180:
        direction = "180 degrees from the reference viewpoint"
    else:
        side = "right" if signed_azimuth > 0 else "left"
        direction = f"{abs(signed_azimuth)} degrees to the {side} of the reference viewpoint"

    if elevation > 0:
        tilt = f"Camera tilt: {elevation} degrees downward."
    elif elevation < 0:
        tilt = f"Camera tilt: {abs(elevation)} degrees upward."
    else:
        tilt = "Keep the camera level."

    # The input prompt already carries the shot distance; the coordinates show direction only.
    components = (round(offset / radius, 3) for offset in (x, y, z))
    coordinates = ", ".join(f"{axis}={value or 0.0:+.3f}" for axis, value in zip("XYZ", components))
    instruction = f"Camera azimuth: {direction}. {tilt}"
    if 75 <= abs(signed_azimuth) <= 105:
        instruction += " Use a near-profile camera view, showing mainly the side of the subject and only a narrow view of the front."
    coordinate_text = (
        f"Camera bearing (0 to 359 degrees): {azimuth} degrees. "
        f"Camera direction from the subject: {coordinates}."
    )
    return instruction, coordinate_text


class H3CameraPromptAdapter(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="H3CameraPromptAdapter",
            display_name="H3 Camera Prompt Adapter",
            category="image/multiangle",
            description="Append the camera direction and tilt to the original Qwen Multiangle Camera prompt. Read the numeric bearing and coordinates separately.",
            inputs=[
                io.String.Input("prompt", display_name="Prompt", force_input=True),
                io.Load3DCamera.Input("camera_info", display_name="Camera Info"),
                io.Boolean.Input(
                    "match_background_view",
                    display_name="Match Background View",
                    default=False,
                    optional=True,
                    tooltip="On: show the existing background from the new camera position. Off: isolate the subject against a plain background.",
                ),
            ],
            outputs=[
                io.String.Output("enhanced_prompt", display_name="Enhanced Prompt"),
                io.String.Output("camera_coordinates", display_name="Camera Coordinates"),
            ],
        )

    @classmethod
    def execute(cls, prompt, camera_info, match_background_view=False):
        instruction, coordinates = _camera_details(camera_info)
        if instruction:
            if match_background_view:
                background = "Show the existing background from the new camera position, with perspective and visibility consistent with that viewpoint."
            else:
                background = "Remove the original background and isolate the subject against a plain, uniform background."
            instruction = f"{instruction}\n{background}"
        enhanced_prompt = f"{prompt}\n{instruction}" if prompt and instruction else prompt or instruction
        return io.NodeOutput(enhanced_prompt, coordinates)


class H3CameraPromptExtension(ComfyExtension):
    async def get_node_list(self):
        return [H3CameraPromptAdapter]


async def comfy_entrypoint():
    return H3CameraPromptExtension()
