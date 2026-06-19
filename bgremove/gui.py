import gradio as gr
from PIL import Image
from pathlib import Path
import tempfile
import os
from bgremove.utils.config import setup_portable_environment

# Ensure environment is isolated BEFORE other imports
MODELS_DIR, CACHE_DIR = setup_portable_environment()

from bgremove.api.service import remove_background


def process_image(image, quality, background, shadow, format):
    if image is None:
        return None, "Please upload an image."

    # Save input to temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)
        tmp_path = Path(tmp.name)

    output_path = tmp_path.with_name(f"output.{format}")

    try:
        result = remove_background(
            image_path=tmp_path,
            output_path=output_path,
            quality=quality.lower(),
            background=background if background != "Transparent" else "transparent",
            shadow=shadow.lower(),
            format=format.lower(),
            device="auto",
        )

        output_image = Image.open(result.output_path)
        report = f"Model used: {result.model_used}\nQuality Score: {result.quality_score:.2f}\nHalo Risk: {result.halo_risk}"
        return output_image, report
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        # Cleanup
        if tmp_path.exists():
            os.unlink(tmp_path)


def launch_gui():
    with gr.Blocks(title="Background Remover Pro") as demo:
        gr.Markdown("# 🚀 Background Remover Pro")
        gr.Markdown("Production-grade background removal powered by BiRefNet and Guided Filter Matting.")

        with gr.Row():
            with gr.Column():
                input_img = gr.Image(type="pil", label="Input Image")

                with gr.Accordion("Settings", open=True):
                    quality = gr.Radio(["Fast", "Balanced", "Pro", "Max"], value="Pro", label="Processing Quality")
                    background = gr.Dropdown(
                        ["Transparent", "White", "Black", "#f0f0f0"], value="Transparent", label="Background"
                    )
                    shadow = gr.Radio(["None", "Drop", "Soft", "Auto"], value="Auto", label="Shadow Effect")
                    img_format = gr.Radio(["PNG", "JPG", "WEBP"], value="PNG", label="Output Format")

                submit_btn = gr.Button("Remove Background", variant="primary")

            with gr.Column():
                output_img = gr.Image(label="Result")
                status_text = gr.Textbox(label="Status & Report", interactive=False)

        submit_btn.click(
            process_image,
            inputs=[input_img, quality, background, shadow, img_format],
            outputs=[output_img, status_text],
        )

        gr.Examples(examples=[], inputs=input_img)  # You can add local images here if available

    demo.launch()


if __name__ == "__main__":
    launch_gui()
