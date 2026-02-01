from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime
from typing import List
from ..models import (
    VendaCreate, 
    VendaUpdate,
    VendaResponse, 
    TotalDiarioResponse,
    TotalMensalResponse
)
from ..database import get_supabase_client

router = APIRouter()


@router.get("/vendas", response_model=List[VendaResponse])
async def listar_vendas(data_filtro: date = Query(..., description="Data para filtrar vendas")):
    """
    Lista todas as vendas de uma data específica.
    Ordenado por horário de criação (mais antigos primeiro).
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("*")\
            .eq("data", data_filtro.isoformat())\
            .order("created_at", desc=False)\
            .execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar vendas: {str(e)}")


@router.get("/vendas/mes/{mes_ano}", response_model=List[VendaResponse])
async def listar_vendas_mes(mes_ano: str):
    """
    Lista todas as vendas de um mês específico.
    Formato mes_ano: YYYY-MM (exemplo: 2026-01)
    """
    try:
        supabase = get_supabase_client()
        
        datetime.strptime(mes_ano, "%Y-%m")
        
        response = supabase.table("vendas")\
            .select("*")\
            .gte("data", f"{mes_ano}-01")\
            .lt("data", f"{mes_ano}-32")\
            .order("data", desc=True)\
            .order("created_at", desc=False)\
            .execute()
        
        return response.data
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato inválido. Use YYYY-MM (exemplo: 2026-01)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar vendas: {str(e)}")


@router.post("/vendas", response_model=VendaResponse, status_code=201)
async def criar_venda(venda: VendaCreate):
    """
    Cria uma nova venda.
    Valida se a data não é futura.
    """
    hoje = date.today()
    if venda.data > hoje:
        raise HTTPException(
            status_code=400, 
            detail=f"Data não pode ser futura. Data máxima: {hoje.isoformat()}"
        )
    
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .insert({
                "data": venda.data.isoformat(),
                "item": venda.item,
                "preco": float(venda.preco)
            })\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar venda")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar venda: {str(e)}")


@router.put("/vendas/{venda_id}", response_model=VendaResponse)
async def atualizar_venda(venda_id: str, venda: VendaUpdate):
    """
    Atualiza uma venda existente.
    Apenas campos fornecidos serão atualizados.
    """
    try:
        supabase = get_supabase_client()
        
        update_data = {}
        if venda.item is not None:
            update_data["item"] = venda.item
        if venda.preco is not None:
            update_data["preco"] = float(venda.preco)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        response = supabase.table("vendas")\
            .update(update_data)\
            .eq("id", venda_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar venda: {str(e)}")


@router.delete("/vendas/{venda_id}", status_code=204)
async def deletar_venda(venda_id: str):
    """
    Deleta uma venda permanentemente.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .delete()\
            .eq("id", venda_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar venda: {str(e)}")


@router.get("/vendas/total/dia/{data}", response_model=TotalDiarioResponse)
async def obter_total_dia(data: date):
    """
    Retorna o total faturado e quantidade de itens vendidos em um dia específico.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("preco")\
            .eq("data", data.isoformat())\
            .execute()
        
        vendas = response.data
        total = sum(float(v["preco"]) for v in vendas)
        quantidade = len(vendas)
        
        return {
            "data": data,
            "total_faturado": total,
            "quantidade_itens": quantidade
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular total: {str(e)}")


@router.get("/vendas/total/mes/{mes_ano}", response_model=TotalMensalResponse)
async def obter_total_mes(mes_ano: str):
    """
    Retorna o total faturado e quantidade de itens vendidos em um mês específico.
    Formato: YYYY-MM (exemplo: 2026-01)
    """
    try:
        datetime.strptime(mes_ano, "%Y-%m")
        
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("preco")\
            .gte("data", f"{mes_ano}-01")\
            .lt("data", f"{mes_ano}-32")\
            .execute()
        
        vendas = response.data
        total = sum(float(v["preco"]) for v in vendas)
        quantidade = len(vendas)
        
        return {
            "mes": mes_ano,
            "total_faturado": total,
            "quantidade_itens": quantidade
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato inválido. Use YYYY-MM")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular total: {str(e)}")