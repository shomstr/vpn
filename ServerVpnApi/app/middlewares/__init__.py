from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

