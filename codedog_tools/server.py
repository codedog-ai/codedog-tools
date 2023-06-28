import gradio as gr
from version import VERSION

from codedog_tools.ui import caseparser_ui, story_ui

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(f"# AI小工具  v{VERSION}")

    with gr.Tab(label="用户故事分析"):
        story_ui.render()
    # with gr.Tab(label="生成测试用例"):
    # caseparser_ui.render()


def start():
    ui.launch(debug=True, share=False)


if __name__ == "__main__":
    start()
