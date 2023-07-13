import gradio as gr
import uvicorn
from fastapi import FastAPI

from codedog_tools.ui import story_ui
from codedog_tools.version import VERSION

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(f"# 小工具 v{VERSION}")

    with gr.Tab(label="用户故事分析"):
        story_ui.render()


app = FastAPI()
app = gr.mount_gradio_app(app, ui, path="/")


def main():
    uvicorn.run("codedog_tools.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
