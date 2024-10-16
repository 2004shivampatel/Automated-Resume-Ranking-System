from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Resume(BaseModel):
    filename: str
    content: str

class RankRequest(BaseModel):
    job_description: str
    resumes: List[Resume]

@app.post("/rank-resumes")
def rank_resumes(request: RankRequest):
    ranked_resumes = sorted(
        request.resumes, key=lambda x: len(x.content), reverse=True
    )
    results = [{"Resume": r.filename, "Score": len(r.content)} for r in ranked_resumes]
    return {"ranked_resumes": results}
