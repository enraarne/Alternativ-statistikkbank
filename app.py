import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

UDIR_API_URL = os.getenv(
    "UDIR_API_URL",
    "https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/VGO/ResultatFagV/2/5/data",
)
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
    if origin.strip()
]
TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

app = FastAPI(title="Statistikkbanken Demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")


class StatisticsRequest(BaseModel):
    radSti: str = "F"
    payload: str


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/statistikk")
async def statistikk(request: StatisticsRequest) -> JSONResponse:
    upstream_url = httpx.URL(UDIR_API_URL).copy_merge_params({"radSti": request.radSti})

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(
                str(upstream_url),
                content=request.payload,
                headers={
                    "Content-Type": "text/plain",
                    "Accept": "application/json, text/plain, */*",
                },
            )
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {error}") from error

    content_type = response.headers.get("content-type", "")
    response_text = response.text

    try:
        parsed_body = response.json()
    except json.JSONDecodeError:
        parsed_body = response_text

    return JSONResponse(
        status_code=response.status_code,
        content={
            "upstream": {
                "url": str(upstream_url),
                "status": response.status_code,
                "contentType": content_type,
            },
            "body": parsed_body,
            "rawText": response_text,
        },
    )
