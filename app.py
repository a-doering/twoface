import gradio as gr
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from twoface.face_align import FaceAligner

# Create an FaceLandmarker object.
base_options = python.BaseOptions(
    model_asset_path="models/mediapipe/face_landmarker_v2_with_blendshapes.task"
)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(options)


fa = FaceAligner(detector)


def generate_image(img_a, img_b, zoom):
    img_a = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_a)
    out_a = fa.align(img_a, zoom=zoom)
    img_b = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_b)
    out_b = fa.align(img_b, zoom=zoom)

    return np.hstack(
        (out_a[:, 0 : out_a.shape[1] // 2], out_b[:, out_b.shape[1] // 2 :])
    )


my_theme = gr.Theme.from_hub("gstaff/xkcd")

with gr.Blocks(theme=my_theme, title="TwoFace") as demo:
    gr.Markdown("# TwoFace")
    gr.Markdown("Combine the faces from two different photos that you upload.")
    with gr.Row():
        with gr.Column():
            image_input_a = gr.Image(label="Image containing left side of face")
            image_input_b = gr.Image(label="Image containing right side of face")
            zoom = gr.Slider(
                minimum=-0.08,
                maximum=0.08,
                step=0.01,
                value=0.0,
                label="Zoom",
                info="<-- zoom out | (zoom not linear) | zoom in -->",
            )
        image_output = gr.Image()
    image_button = gr.Button("Generate TwoFace")
    image_button.click(
        generate_image,
        inputs=[image_input_a, image_input_b, zoom],
        outputs=image_output,
    )

    image_button_flip = gr.Button("Generate TwoFace with left and right sides flipped")
    image_button_flip.click(
        generate_image,
        inputs=[image_input_b, image_input_a, zoom],
        outputs=image_output,
    )

    gr.Markdown("Created by [a-doering](https://github.com/a-doering).")

demo.queue()
demo.launch(server_name="0.0.0.0", server_port=7860)
