import os
from supabase import create_client, Client
from typing import Optional

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """
    Retorna uma instância do cliente Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)


async def test_connection() -> bool:
    """
    Testa conexão com Supabase.
    Retorna True se conectou, False caso contrário.
    """
    try:
        supabase = get_supabase_client()
        # Tenta fazer uma query simples
        supabase.table("vendas").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Erro ao conectar no Supabase: {str(e)}")
        return False