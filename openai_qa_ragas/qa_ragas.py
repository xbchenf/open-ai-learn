from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.langchain.evalchain import RagasEvaluatorChain
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
import  os
import openai
import  time

openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = 'ls__e77bbf50f90949e082e66305f4b8972d'
os.environ['LANGCHAIN_PROJECT'] = 'langchain-openai-langsmith01'

#定义LLM模型、Embedding模型
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
embedding_model = OpenAIEmbeddings()

#准备本地知识库
doc_list = """
1. 美国总统是谁？
   拜登
2. 印度人吃饭的工具是什么？
   右手
3. CBA是什么？
   CBA是指中国男子篮球职业联赛（China Basketball Association），这是中国最高等级的篮球联赛
4. 佛教起源哪里？
   古印度
5. 美国的职业篮球赛叫什么？
   NBA，全称为National Basketball Association，中文名为美国职业篮球联赛，是北美地区的最高等级职业篮球赛事
"""

#文档拆分分块
text_spliter = CharacterTextSplitter(separator="\n",
                                     chunk_size=500,
                                     chunk_overlap=50,
                                     length_function=len)
chunks = text_spliter.split_text(doc_list)

#文档embedding到向量数据库
vectorstore = FAISS.from_texts(texts=chunks,
                                  embedding=embedding_model)

#构建chain链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
)

## 定义要测试的样本问题，可以定义多个，这里方便看测试效果，暂只定义1个
eval_questions = [
    "美国总统是谁？"
]

eval_answers = [
    "拜登"
]

examples = [
    {"query": q, "ground_truths": [eval_answers[i]]}
    for i, q in enumerate(eval_questions)
]

## 看一下从知识库里搜索出来的答案
result = qa_chain({"query": eval_questions[0]})
print(result)
time.sleep(30)

##评估测试
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_relevancy,
)

# 1.创建"忠诚度"评估chains链
faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
# 2.创建“答案相关性”评估链
answer_rel_chain = RagasEvaluatorChain(metric=answer_relevancy)
# 3.创建“上下文精准度”评估链
context_pre_chain = RagasEvaluatorChain(metric=context_precision)
# 4.创建“上下文召回率”评估链
context_recall_chain = RagasEvaluatorChain(metric=context_recall)
# 5.创建“上下文相关性”评估链
context_relevancy_chain = RagasEvaluatorChain(metric=context_relevancy)

##预测值
predict = qa_chain.batch(examples)
##预测值与真实值对比
result1 = faithfulness_chain.evaluate(examples,predict)
print(result1)
time.sleep(30)

result2 = answer_rel_chain.evaluate(examples,predict)
print(result2)
time.sleep(30)

result3 = context_pre_chain.evaluate(examples,predict)
print(result3)
time.sleep(30)

result4 = context_recall_chain.evaluate(examples,predict)
print(result4)
time.sleep(30)

result5 = context_relevancy_chain.evaluate(examples,predict)
print(result5)