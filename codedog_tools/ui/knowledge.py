import gradio as gr

kbase = KnowledgeBase()

with gr.Blocks() as knowledge_ui:
    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                user_story_docs = gr.UploadButton(label="用户故事相关文档", file_count="multiple", file_types="text")
        with gr.Column():
            with gr.Row():
                build = gr.Button(value="重建知识库")
            with gr.Row():
                status = gr.JSON(value={"code": 0}, show_label=False)

    user_story_docs.click(
        kbase.build({"user": user_story_docs}),
        inputs=[user_story_docs],
        outputs=[status],
    )
