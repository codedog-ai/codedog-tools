import json
from typing import List

from genson import SchemaBuilder
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser

PYDANTIC_FORMAT_INSTRUCTIONS = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```
{schema}
```"""


class CaseParser:
    def parse(self, input_model: str, output_model: str, description: str, cases: List[List[str]]):
        schema = self.build_schema(input_model, output_model)
        template = self.build_template(schema, description)
        prompt = PromptTemplate(input_variables=["input", "output"], template=template)

        return "", {}
