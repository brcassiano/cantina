from supabase import create_client, Client
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

@lru_cache()
def get_supabase_client() -> Client:
    """
    Retorna cliente Supabase singleton com connection pooling.
    A conexão é reutilizada entre as requisições.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")
    
    return create_client(url, key)


async def test_connection():
    """Testa conexão com Supabase"""
    try:
        client = get_supabase_client()
        response = client.table("vendas").select("count", count="exact").limit(0).execute()
        return True
    except Exception as e:
        print(f"Erro ao conectar no Supabase: {e}")
        return False