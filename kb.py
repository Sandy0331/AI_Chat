import chromadb
from chromadb.utils import embedding_functions

# 配置中文向量模型
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "BAAI/bge-small-zh-v1.5"
)

# 创建本地文件型向量库
client = chromadb.PersistentClient(path="./chroma_db")

# 创建集合
collection = client.get_or_create_collection(
    name="company_kb",
    embedding_function=ef
)

# 增加数据
docs = [
    "报销流程：员工提交报销单 → 直属主管审批 → 财务复核打款，周期一般 3 个工作日。",
    "年假规则：入职满一年享 5 天年假，每多一年增加 1 天，上限 15 天。",
    "加班规定：工作日加班 1.5 倍时薪，周末 2 倍，法定节假日 3 倍，需提前在系统申请。",
]

collection.add(
    ids = ["doc1","doc2","doc3"],
    documents = docs
)

#print(f"知识库已入库，共{collection.count()}条")
print("知识库已入库，共", collection.count(), "条")