from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import vendas, produtos, analytics
from .database import test_connection
import os

app = FastAPI(
    title="Cantina Escolar API",
    description="API para gerenciamento de vendas de cantina escolar",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a aplicação"""
    print("🚀 Iniciando Cantina Escolar API...")
    
    connection_ok = await test_connection()
    if connection_ok:
        print("✅ Conexão com Supabase estabelecida")
    else:
        print("❌ Falha ao conectar com Supabase")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Cantina Escolar API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "vendas": "/api/v1/vendas",
            "produtos": "/api/v1/produtos",
            "analytics": "/api/v1/analytics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "environment": os.getenv("ENVIRONMENT", "production")}


# Incluir routers
app.include_router(vendas.router, prefix="/api/v1", tags=["Vendas"])
app.include_router(produtos.router, prefix="/api/v1", tags=["Produtos"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])