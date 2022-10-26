"""
Main FastAPI server instance
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/help-ua-docs/docs", openapi_url="/help-ua-docs/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
