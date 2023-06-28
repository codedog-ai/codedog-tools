import gradio as gr

from codedog_tools.story import StoryReview

story = StoryReview()

default_story = "作为运维人员，我希望能自动生成主机监控列表，以便我能无脑且快速的完成主机数据的统一监控"
default_ac = """1、所有安装oneAgent的主机都会出现在主机监控列表
2、主机列表显示最近两小时被oneAgent监控的所有主机
3、主机列表中包含特定的主机属性字段和指标数据"""


with gr.Blocks() as story_ui:
    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                user_story = gr.Textbox(label="用户故事", value=default_story, lines=4, max_lines=30)
            with gr.Row():
                acceptance_criteria = gr.Textbox(label="验收标准", value=default_ac, lines=4, max_lines=30)
        with gr.Column():
            with gr.Row():
                review = gr.Button(value="评审")
            with gr.Row():
                status = gr.JSON(value={"code": 0}, show_label=False)
    with gr.Row():
        overall_comment = gr.Textbox(label="整体评价", value="", lines=4, max_lines=30, interactive=False)
    with gr.Row():
        illustration = gr.Textbox(label="澄清问题", value="", lines=4, max_lines=30, interactive=False)
    with gr.Row():
        mandays = gr.Textbox(label="工作量分析", value="", lines=4, max_lines=30, interactive=False)

    review.click(
        story.review,
        inputs=[user_story, acceptance_criteria],
        outputs=[overall_comment, illustration, mandays, status],
    )
