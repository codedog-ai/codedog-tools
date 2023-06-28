import gradio as gr

from codedog_tools.story import StoryReview

story = StoryReview()


with gr.Blocks() as story_ui:
    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                user_story = gr.Textbox(label="用户故事", value="", lines=4, max_lines=30)
            with gr.Row():
                acceptance_criteria = gr.Textbox(label="验收标准", value="", lines=4, max_lines=30)
        with gr.Column():
            with gr.Row():
                review = gr.Button(value="评审")
            with gr.Row():
                status = gr.JSON(value={"code": 0}, show_label=False)
    with gr.Row():
        overall_comment = gr.Textbox(label="整体评价", value="", lines=4, max_lines=30, interactive=False)
    with gr.Row():
        illustration_questions = gr.Textbox(label="澄清问题", value="", lines=4, max_lines=30, interactive=False)
    with gr.Row():
        mandays_estimate = gr.Textbox(label="工作量评估", value="", lines=4, max_lines=30, interactive=False)

    review.click(
        story.review,
        inputs=[user_story, acceptance_criteria],
        outputs=[overall_comment, illustration_questions, mandays_estimate, status],
    )
