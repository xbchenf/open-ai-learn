
from langchain.chat_models import ChatOpenAI
from config.keys import Keys
from langchain.embeddings import OpenAIEmbeddings

# 核心关注点temperature=0
# 对于知识库我们要求内容要严谨，不可随意发挥
def get_openai_model():
    llm_model = ChatOpenAI(openai_api_key=Keys.OPENAI_API_KEY,
                           model_name=Keys.MODEL_NAME,
                           temperature=0)
    return llm_model


def get_openaiEmbedding_model():
    return OpenAIEmbeddings(openai_api_key=Keys.OPENAI_API_KEY)

