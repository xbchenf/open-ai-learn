from document import ContentType

# 定义模型父类
class Model:
    def make_text_prompt(self, text: str, target_language: str) -> str:
        #return f"翻译为{target_language}：{text}"
        return f"Text: '{text}'\nTranslation (to {target_language}):"
        #return PromptTemplate.human_text_prompt(text, target_language)

    def make_table_prompt(self, table: str, target_language: str) -> str:
        #return f"翻译为{target_language}，保持间距（空格，分隔符），以表格形式返回：\n{table}"
        return f"Table: '{table}'\nTranslation (to {target_language}):\n"
        #return PromptTemplate.human_table_prompt(table, target_language)

    def translate_prompt(self, content, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), target_language)
        
    @staticmethod
    def get_system_prompt():
        return ""

    # 留给子类实现
    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
