import gradio as gr
from version import VERSION

from codedog_tools.ui import story_ui

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(f"# CodeDog Tools  v{VERSION}")

    with gr.Tab(label="用户故事分析"):
        story_ui.render()


def start():
    ui.launch(debug=True, share=False)


if __name__ == "__main__":
    start()
