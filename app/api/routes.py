from fastapi import APIRouter, HTTPException
from app.api.models import Query, Response, SummaryStats
from app.services.rag_service import rag_service
from app.services.analysis_service import analysis_service

router = APIRouter()

@router.post("/chat", response_model=Response)
async def chat_endpoint(query: Query):
    try:
        result = rag_service.query(query.text)
        
        sources = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in result.get("source_documents", [])
        ]
        
        additional_info = {}
        if any(word in query.text.lower() for word in ['spending', 'cost', 'price', 'amount']):
            additional_info["spending_analysis"] = analysis_service.analyze_spending(
                result.get("source_documents")
            )
        
        return Response(
            answer=result["result"],
            sources=sources,
            additional_info=additional_info
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary", response_model=SummaryStats)
async def get_summary_stats():
    try:
        return analysis_service.get_summary_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/load")
async def load_data(background_tasks: BackgroundTasks):
    """Endpoint to trigger data loading in the background"""
    try:
        background_tasks.add_task(data_loader.load_csv_data)
        return {"message": "Data loading process started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/status")
async def check_data_status():
    """Check the status of data in MongoDB"""
    try:
        return data_loader.verify_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))