from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Database
from app.services.rag_service import rag_service
from app.utils.data_loader import data_loader
from config.settings import settings

app = FastAPI(title="Procurement RAG Chatbot")

@app.on_event("startup")
async def startup_event():
    """Initialize database connection and load data if needed"""
    Database.connect()
    try:
        # Attempt to load data if collection is empty
        data_loader.load_csv_data()
    except Exception as e:
        print(f"Warning: Data loading failed: {e}")
    
    # Initialize RAG pipeline
    rag_service.initialize_pipeline()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    Database.close()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )