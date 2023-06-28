import json
import os
import time
import traceback
from typing import Tuple

from langchain import LLMChain, PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI

with open("env.json") as f:
    env: dict = json.load(f)
    os.environ.update(env["env"])

template = """扮演一名资深产品经理，对以下用户故事进行分析：
用户故事:
```
{{story}}
```
验收标准:
```
{{standard}}
```

首先，{overview_requirement}

其次，{illustration_requirement}

最后，{mandays_requirement}

{format}
""".format(
    format="""请使用markdown格式进行回答:""",
    overview_requirement="""简要概括你对这份用户故事以及验收标准的看法""",
    illustration_requirement="""如果你认为内容中有表述不清的地方，请提出一些问题来协助我们澄清，我会将这些问题转述给产品经理""",
    mandays_requirement="""请给出你对该用户故事工作量和需求难度的分析""",
)


class StoryReview:
    def __init__(self):
        prompt = PromptTemplate(input_variables=["story", "standard"], template=template)

        llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            openai_api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
            openai_api_version="2023-05-15",
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID", "gpt-35-turbo"),
            model="gpt-3.5-turbo",
            temperature=0.2,
        )

        self.storychain = LLMChain(llm=llm, prompt=prompt)

    def review(self, story: str, standard: str) -> Tuple[str, str, str, str]:
        args = {"story": story, "standard": standard}
        telemetry = {"code": 0}

        try:
            with get_openai_callback() as cb:
                t = time.time()
                result: str = self.storychain.run(args)
                telemetry["tokens"] = cb.total_tokens
                telemetry["cost"] = f"$ {cb.total_cost:.4f}"
                telemetry["time_usage"] = f"{int(time.time() - t)}s"
        except Exception as e:
            telemetry["code"] = 1
            telemetry["trace"] = traceback.format_exc()
            telemetry["error"] = str(e)
            result = ""

        return result, telemetry
