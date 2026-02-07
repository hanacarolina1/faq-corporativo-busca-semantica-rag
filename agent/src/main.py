from fastapi import FastAPI
from src.api.routers import faq, health

app = FastAPI(title="FAQ Corporativo - Agente Semântico")

app.include_router(health.router)
#app.include_router(faq.router)