from langchain.chat_models import ChatOpenAI


from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from document import ContentType
from utils import LOG

class TranslationChain:
    def __init__(self, content, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        # System prompt
        system_prompt = """
        You are an advanced translation assistant, specialized in translating between various languages. Your task is to:

        - Accurately detect the source language.
        - Translate the content as precisely as possible.
        - Preserve original formatting such as tables, spacing, punctuation, and special structures.

        Here are some examples to guide you:

        Example 1:
        Text: 'Hello, how are you?'
        Translation (to Spanish): Hola, ¿cómo estás?

        Example 2:
        Text: 'Je suis heureux.'
        Translation (to Japanese): 私は幸せです。

        Note: For text-like content, translate content accurately without adding or removing any punctuation or symbols.

        Example 3:
        Table: '[Name, Age] [John, 25] [Anna, 30]'
        Translation (to Chinese): [姓名, 年龄] [约翰, 25] [安娜, 30]

        Note: For table-like content, keep the format using square brackets with commas as separators. Return ONLY the translated content enclosed within brackets without any additional explanations. Specifically, when translating into Japanese, do not translate commas(,) into Japanese punctuation "、" or "、".

        Now, proceed with the translations, detecting the source language and translating to the specified target language.

        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
        
        # Human Prompts
        ## 文本的Prompt
        human_text_template =  "Text: '{text}'\nTranslation (to {target_language}):"
        human_massage_prompt =HumanMessagePromptTemplate.from_template(human_text_template)
        self.chat_text_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_massage_prompt]
        )       
        ## 表格的Prompt
        human_table_template =  "Table: '{table}'\nTranslation (to {target_language}):\n"
        human_massage_prompt =HumanMessagePromptTemplate.from_template(human_table_template)

        self.chat_table_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_massage_prompt]
        )       
        
        # LLM
        ## 指定调用的模型
        self.chat = ChatOpenAI(model_name = model_name, temperature= 0, verbose= verbose)

    # 定义run函数，用于执行翻译任务
    def run(self, content: str, target_language: str, verbose=True) -> (str, bool):
        # 初始化结果为空字符串
        result = ""
        try:
            # 当内容类型为文本时
            if content.content_type == ContentType.TEXT:
                # 创建LLMChain对象，使用文本提示模板
                self.chain = LLMChain(llm=self.chat, prompt=self.chat_text_prompt_template, verbose=verbose)
                # 调用run方法执行翻译任务
                result = self.chain.run({
                    "text": content.original,
                    "target_language": target_language,
                })
            # 当内容类型为表格时
            elif content.content_type == ContentType.TABLE:
                # 创建LLMChain对象，使用表格提示模板
                self.chain = LLMChain(llm=self.chat, prompt=self.chat_table_prompt_template, verbose=verbose)
                # 调用run方法执行翻译任务
                result = self.chain.run({
                    "table": content.get_original_as_str(),
                    "target_language": target_language,
                })

        # 当出现异常时
        except Exception as e:
            # 打印错误日志
            LOG.error(f"An error occurred during translation: {e}")
            # 返回结果和失败标识
            return result, False

            # 返回结果和成功标识
        return result, True

    