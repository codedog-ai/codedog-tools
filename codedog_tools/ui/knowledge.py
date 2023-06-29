import gradio as gr

with gr.Blocks() as knowledge_ui:
    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                user_story_docs = gr.UploadButton(label="用户故事相关文档", file_count="multiple", file_types="text")
            with gr.Row():
                test_cases_docs = gr.UploadButton(label="测试用例相关文档", file_count="multiple", file_types="text")
        with gr.Column():
            with gr.Row():
                review = gr.Button(value="重建知识库")
            with gr.Row():
                status = gr.JSON(value={"code": 0}, show_label=False)
