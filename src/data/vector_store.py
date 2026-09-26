# import os
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from src.core.config import Config

# class VectorStoreManager:
#     def __init__(self):
#         # استخدام Embeddings محلية ومجانية ممتازة للغة العربية
#         self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

#     def build_database(self):
#         """قراءة اللوائح وبناء قاعدة البيانات المتجهة ChromaDB"""
#         if not os.path.exists(Config.REGULATIONS_DIR):
#             os.makedirs(Config.REGULATIONS_DIR)

#         loader = PyPDFDirectoryLoader(Config.REGULATIONS_DIR)
#         docs = loader.load()

#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
#         splits = text_splitter.split_documents(docs)

#         vectorstore = Chroma.from_documents(
#             documents=splits,
#             embedding=self.embeddings,
#             persist_directory=Config.CHROMA_DB_DIR
#         )
#         return vectorstore

#     def get_retriever(self):
#         """استرجاع قاعدة البيانات الجاهزة"""
#         vectorstore = Chroma(
#             persist_directory=Config.CHROMA_DB_DIR,
#             embedding_function=self.embeddings
#         )
#         return vectorstore.as_retriever(search_kwargs={"k": 3})


import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.config import Config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    def build_database(self):
        """قراءة اللوائح وبناء قاعدة البيانات المتجهة ChromaDB"""
        if not os.path.exists(Config.REGULATIONS_DIR):
            os.makedirs(Config.REGULATIONS_DIR)

        # قراءة ملفات PDF وملفات TXT
        pdf_loader = DirectoryLoader(Config.REGULATIONS_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader(Config.REGULATIONS_DIR, glob="./*.txt", loader_cls=TextLoader)

        docs = pdf_loader.load() + txt_loader.load()

        if not docs:
            print("⚠️ تحذير: لم يتم العثور على أي ملفات نصية داخل مجلد regulations!")
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        if not splits:
            print("⚠️ تحذير: النصوص المستخرجة فارغة!")
            return None

        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=Config.CHROMA_DB_DIR
        )
        return vectorstore

    def get_retriever(self):
        """استرجاع قاعدة البيانات الجاهزة"""
        vectorstore = Chroma(
            persist_directory=Config.CHROMA_DB_DIR,
            embedding_function=self.embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": 2})