import gradio as gr

from codedog_tools.ui import story_ui

from . import VERSION

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(f"# CodeDog Tools {VERSION}")

    with gr.Tab(label="用户故事分析"):
        story_ui.render()


def start():
    ui.launch(debug=True, share=False)
