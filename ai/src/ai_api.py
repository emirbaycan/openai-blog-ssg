from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.app import process_title

app = FastAPI()

class ProcessRequest(BaseModel):
    title_id: int

@app.post("/generate/")
def generate_blog(req: ProcessRequest):
    try:
        process_title(req.title_id)
        return {"status": "ok", "message": f"Başlık işlendi: {req.title_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
