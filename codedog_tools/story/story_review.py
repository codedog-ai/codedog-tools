import json
import os
import time
import traceback
from typing import Tuple

from langchain import LLMChain, PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI

input_part = """请作为需求分析专家协助我对以下用户故事进行分析：
用户故事:
```
{{story}}
```
验收标准:
```
{{standard}}
```

{requirement}

{format}
"""

format_part = """请给出你的回答:"""

overview_requirement = """简要概括你对这份用户故事以及验收标准的看法"""

illustration_requirement = """如果你认为这份用户故事以及验收标准有表述的不清晰的地方，请提出一些问题来协助我们澄清"""

mandays_requirement = """请给出你对该用户故事工作量和需求难度的分析"""

overview_template = input_part.format(requirement=overview_requirement, format=format_part)
illustration_template = input_part.format(requirement=illustration_requirement, format=format_part)
mandays_template = input_part.format(requirement=mandays_requirement, format=format_part)


class StoryReview:
    def __init__(self):
        prompt_overview = PromptTemplate(input_variables=["story", "standard"], template=overview_template)
        prompt_illustration = PromptTemplate(input_variables=["story", "standard"], template=illustration_template)
        prompt_mandays = PromptTemplate(input_variables=["story", "standard"], template=mandays_template)
        llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            openai_api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
            openai_api_version="2023-05-15",
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID", "gpt-35-turbo"),
            model="gpt-3.5-turbo",
            temperature=0.2,
        )

        self.overview_chain = LLMChain(llm=llm, prompt=prompt_overview)
        self.illustration_chain = LLMChain(llm=llm, prompt=prompt_illustration)
        self.mandays_chain = LLMChain(llm=llm, prompt=prompt_mandays)

    def review(self, story: str, standard: str, doc) -> Tuple[str, str, str, str]:
        args = {"story": story, "standard": standard}
        telemetry = {"code": 0}

        qa = self.build_qa_chain(doc)
        illustration_chain = qa is not None and qa or self.illustration_chain

        specification = self.process_doc(doc)
        if specification:
            chain = self.build_qa_chain(speicification=specification)

        try:
            with get_openai_callback() as cb:
                t = time.time()
                # overview: str = self.overview_chain.run(args)
                overview = ""
                illustration: str = illustration_chain.run(args)
                mandays: str = self.mandays_chain.run(args)

                telemetry["tokens"] = cb.total_tokens
                telemetry["cost"] = f"$ {cb.total_cost:.4f}"
                telemetry["time_usage"] = f"{int(time.time() - t)}s"

            return overview, illustration, mandays, json.dumps(telemetry)
        except Exception as e:
            telemetry["code"] = 1
            telemetry["trace"] = traceback.format_exc()
            telemetry["error"] = str(e)

        return "", "", "", telemetry

    def process_doc(self, doc):
        pass
