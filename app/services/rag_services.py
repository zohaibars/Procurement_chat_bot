from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from config.settings import settings
from app.core.database import Database
from app.utils.helpers import prepare_documents, batch_process_chunks

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.qa_chain = None
        
    def initialize_pipeline(self):
        chunks = prepare_documents(Database.connect())
        valid_chunks = batch_process_chunks(chunks, self.embeddings)
        
        vectorstore = self._initialize_vectorstore(valid_chunks)
        retriever = self._configure_retriever(vectorstore)
        self.qa_chain = self._create_qa_chain(retriever)
        
    def _initialize_vectorstore(self, chunks):
        if os.path.exists(settings.CHROMA_DB_PATH):
            return Chroma(
                persist_directory=settings.CHROMA_DB_PATH,
                embedding_function=self.embeddings
            )
        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.CHROMA_DB_PATH
        )
    
    def _configure_retriever(self, vectorstore):
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.7}
        )
    
    def _create_qa_chain(self, retriever):
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a procurement data analysis expert. Based on the following context and question,
            provide a detailed analysis with specific numbers, dates, and calculations where relevant.
            
            Context: {context}
            
            Question: {question}
            
            Instructions:
            1. Focus on numerical data and trends when present
            2. Include specific purchase orders and departments in your analysis
            3. Mention dates and fiscal years when relevant
            4. If calculations are needed, show your work
            5. If information is missing or unclear, state so explicitly
            
            Answer:"""
        )
        
        chat_llm = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.3,
            max_retries=3
        )
        
        return RetrievalQA.from_chain_type(
            llm=chat_llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def query(self, question: str):
        if not self.qa_chain:
            raise ValueError("RAG pipeline not initialized")
        return self.qa_chain({"query": question})

rag_service = RAGService()