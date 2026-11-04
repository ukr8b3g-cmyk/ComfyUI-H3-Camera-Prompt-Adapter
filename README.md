# H3 Camera Prompt Adapter

[日本語](#日本語)

Change the camera viewpoint of a reference image with **Qwen Multiangle Camera → H3 Camera Prompt Adapter → MiniMax H3**. The adapter keeps the camera node's original prompt and adds camera direction, tilt, and a background instruction. The included workflow uses the MiniMax H3 FL2VA diffusion model and Qwen3-VL **32B** NVFP4/AWQ text encoder with the P-H3-Image LoRA and VAE.

## Requirements and installation

1. Use **ComfyUI 0.44.0 or later** for the included workflow. Version 0.44.0 introduced the built-in [p-h3-image Conditioning node](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0).
2. Install **Qwen Multiangle Camera** by searching for `comfyui-qwenmultiangle` in ComfyUI Manager. The workflow was saved with v0.7.0. [Qwen Multiangle Camera repository](https://github.com/jtydhr88/ComfyUI-qwenmultiangle)
3. Run this command in `ComfyUI/custom_nodes`. Then restart ComfyUI and refresh the browser.

```sh
git clone https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Camera-Prompt-Adapter.git
```

For a Git installation, run `git pull` inside the adapter's folder to update it, then restart ComfyUI. The adapter has no extra Python package dependencies.

## Models

Place the files in the indicated folders under `ComfyUI/models/`, or use your configured model paths. If your copies are in subfolders, select them in the workflow's loaders.

| Role | File | Folder |
| --- | --- | --- |
| MiniMax H3 FL2VA diffusion model | [minimax_h3_fl2va_pruned_int8_convrot.safetensors](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors) | `models/diffusion_models/` |
| Qwen3-VL 32B NVFP4/AWQ text encoder | [qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) | `models/text_encoders/` |
| P-H3-Image VAE | [p-h3-image_vae_int8_convrot.safetensors](https://huggingface.co/PrunaAI/P-H3-Image-Comfy/blob/main/vae/p-h3-image_vae_int8_convrot.safetensors) | `models/vae/` |
| P-H3-Image LoRA | [p-h3-image_lora_bf16.safetensors](https://huggingface.co/PrunaAI/P-H3-Image-Comfy/blob/main/loras/p-h3-image_lora_bf16.safetensors) | `models/loras/` |

The workflow uses text encoder type `minimax` and LoRA model strength `1.0`. [MiniMax H3 model card](https://huggingface.co/Comfy-Org/MiniMax-H3), [P-H3-Image model card](https://huggingface.co/PrunaAI/P-H3-Image-Comfy)

## Example workflow

1. Open [P3_image_MultiangleCamera.json](workflows/P3_image_MultiangleCamera.json) in ComfyUI. Select a reference image in **Load Image** and adjust the camera's horizontal angle, vertical angle, and framing.
2. Leave **Match Background View** on to request the original scene from the new viewpoint. Turn it off to request a plain background. Use **Additional Prompt** for any extra editing instructions.
3. Queue the workflow. **Save Animated WEBP** saves the result to the standard output folder. The sample uses the original camera prompt with the adapter's additions and passes it to **p-h3-image Conditioning**.

| Adapter port | Purpose |
| --- | --- |
| **Prompt** and **Camera Info** | Connect the matching outputs of Qwen Multiangle Camera. |
| **Enhanced Prompt** | Keeps the original prompt, including any `<sks>` prefix, and adds camera and background instructions. |
| **Camera Coordinates** | Reports the 0–359° bearing and normalized XYZ direction relative to the camera target for inspection. |

The adapter measures left and right from the camera's reference viewpoint. The direction is expressed as text and the generated angle can vary. The example uses the camera prompt's framing terms, such as `close-up` or `wide shot`, for shot distance.

## 日本語

**Qwen Multiangle Camera → H3 Camera Prompt Adapter → MiniMax H3** を使って、参照画像を別のカメラ位置から見た画像に編集するワークフローです。アダプターは元のカメラプロンプトを残し、座標から求めた方向、傾き、背景の指示を追記します。サンプルの拡散モデルは MiniMax H3 FL2VA、テキストエンコーダーは Qwen3-VL **32B** NVFP4/AWQ です。画像編集に P-H3-Image の LoRA と VAE を組み合わせます。

### 必要環境と導入

1. 同梱ワークフローには **ComfyUI 0.44.0 以降**が必要です。0.44.0 で標準の p-h3-image Conditioning が追加されました。 [ComfyUI v0.44.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0)
2. ComfyUI Manager で `comfyui-qwenmultiangle` を検索して導入します。サンプルで使用した版は v0.7.0 です。 [Qwen Multiangle Camera](https://github.com/jtydhr88/ComfyUI-qwenmultiangle)
3. `ComfyUI/custom_nodes` で次のコマンドを実行し、ComfyUI を再起動してブラウザーを更新します。

```sh
git clone https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Camera-Prompt-Adapter.git
```

更新時はアダプターのフォルダで `git pull` を実行し、ComfyUI を再起動します。アダプターに追加の Python パッケージは不要です。

### モデルと配置先

[モデル一覧](#models) のリンクから4ファイルを入手し、`ComfyUI/models/` 配下の `diffusion_models/`、`text_encoders/`、`vae/`、`loras/` にそれぞれ置きます。Stability Matrix などで共有モデルパスを設定している場合は、その対応フォルダに置きます。サブフォルダに入れている場合は、ワークフローの各ローダーで選び直してください。テキストエンコーダーの種類は `minimax`、LoRA のモデル強度は `1.0` です。

### ワークフローの使い方

1. [P3_image_MultiangleCamera.json](workflows/P3_image_MultiangleCamera.json) を ComfyUI で開き、**Load Image** で参照画像を選びます。Qwen Multiangle Camera で水平角・垂直角・寄り具合を設定します。
2. **Match Background View** をオンにすると、元の背景を新しいカメラ位置から見せるよう指示します。オフにすると、被写体を無地の背景に置くよう指示します。追加の編集指示は **Additional Prompt** に入力します。
3. 実行すると、**Save Animated WEBP** が標準出力フォルダに保存します。

アダプターの **Prompt** と **Camera Info** にはカメラノードの同名出力を接続します。**Enhanced Prompt** がモデルに渡す文字列です。**Camera Coordinates** では、ターゲットからカメラへの正規化 XYZ と、基準視点からの方位角（0〜359°）を確認できます。左右はカメラの基準視点を基準に表し、生成画像での角度の再現には幅があります。

## License and credits / ライセンスと謝辞

The adapter is licensed under [MIT](LICENSE). The example workflow adapts Comfy Org's [p-h3-image edit template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_p_h3_image_edit.json). Qwen Multiangle Camera is by [jtydhr88](https://github.com/jtydhr88/ComfyUI-qwenmultiangle). Model weights are distributed by their respective publishers under their own terms.

アダプターは [MIT](LICENSE) です。サンプルは Comfy Org の p-h3-image 編集テンプレートを基にしています。Qwen Multiangle Camera の作者は jtydhr88 です。モデルの利用条件は各配布元を参照してください。
