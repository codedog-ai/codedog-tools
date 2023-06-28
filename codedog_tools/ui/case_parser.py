import gradio as gr

from codedog_tools.case.case_parser import CaseParser

input_model = ""
output_model = ""

case_parser = CaseParser()

with gr.Blocks() as caseparser_ui:
    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                input_model = gr.Textbox(label="输入模型", value=input_model, lines=4, max_lines=30)
            with gr.Row():
                output_model = gr.Textbox(label="输出模型", value=output_model, lines=4, max_lines=30)
            with gr.Row():
                description = gr.Textbox(label="场景描述", value=output_model, lines=4, max_lines=30)
        with gr.Column():
            with gr.Row():
                parse = gr.Button(value="生成测试用例")
            with gr.Row():
                status = gr.JSON(value={"code": 0}, show_label=False)
    with gr.Row():
        cases = gr.Dataframe(headers=["输入", "输出"], row_count=(3, 100), col_count=(2, 2), type="array", label="人工测试用例")
    with gr.Row():
        case_data = gr.Textbox(label="解析测试用例", lines=4, max_lines=100, interactive=False)

    parse.click(
        case_parser.parse,
        inputs=[input_model, output_model, description, cases],
        outputs=[case_data, status],
    )
