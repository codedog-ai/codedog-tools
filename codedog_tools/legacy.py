import gradio as gr
import openai
from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

openai.proxy = "127.0.0.1:8081"
openai_api_key = "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"


default_template = """扮演一名资深产品经理，对以下用户故事进行分析：
用户故事:{story}
验收标准:{standard}

请按如下格式回复，中括号代表说明，回复时不要带上中括号

```
- 故事质量: [请按用户故事的清晰程度进行0-1的打分]
- 预计工时: [请按[后端人天]-[前端人天]-[测试人天]给出一个预期工时，所有的开发人员都是一般的初级工程师的工作水平]
- 故事澄清: [如果你认为该用户故事比较清晰，请跳过这一部分，如果你认为该用户故事还有可以完善的细节，请提出一些帮助产品经理澄清该用户故事的问题，最多不超过10个]
```"""

prompt = PromptTemplate(input_variables=["story", "standard"], template=default_template)

llm = ChatOpenAI(temperature=0.9, openai_api_key=openai_api_key)
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)


def convert_extra(extra: list[list]):
    data = {}
    for k, v in extra:
        if not k:
            continue
        k = str(k)
        if not v:
            v = ""
        data[k] = v
    return data


def review(template, story, standard, extra: list[list]):
    extraObject = convert_extra(extra)
    extraObject["story"] = story
    extraObject["standard"] = standard
    chain.prompt = PromptTemplate.from_template(template)
    return chain.run(extraObject)


def reset_template():
    return default_template


with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("## 用户故事AI评审")
    with gr.Row():
        with gr.Column(scale=11):
            template = gr.Textbox(label="prompt", value=default_template, lines=4, max_lines=30)
        with gr.Column():
            submit = gr.Button(value="评审")
            reset = gr.Button(value="重置Prompt")

    with gr.Row():
        with gr.Column(scale=6):
            story = gr.Textbox(label="用户故事(story)", placeholder="用户故事", lines=5, max_lines=5)
        with gr.Column(scale=6):
            standard = gr.Textbox(label="验收标准(standard)", placeholder="用户故事验收标准", lines=5, max_lines=5)
    with gr.Row():
        extra = gr.DataFrame(label="额外参数", headers=["参数名称", "参数值"], col_count=(2, "fixed"), type="array")
    with gr.Row():
        response = gr.TextArea(label="评审结果")

        submit.click(review, inputs=[template, story, standard, extra], outputs=[response])
        reset.click(reset_template, outputs=template)


# demo.launch(debug=True,share=False)

app = FastAPI()

app = gr.mount_gradio_app(app, demo, path="/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
