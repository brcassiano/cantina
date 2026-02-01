from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal
from datetime import datetime
from uuid import UUID
from ..database import get_supabase_client

router = APIRouter()


# ==================== SCHEMAS ====================

class ProdutoCreate(BaseModel):
    """Schema para criar produto"""
    nome: str = Field(..., min_length=1, max_length=100)
    categoria: Optional[str] = Field(None, max_length=50)
    preco_padrao: condecimal(max_digits=10, decimal_places=2, gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Suco de Laranja",
                "categoria": "bebida",
                "preco_padrao": 5.50
            }
        }


class ProdutoUpdate(BaseModel):
    """Schema para atualizar produto"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    categoria: Optional[str] = Field(None, max_length=50)
    preco_padrao: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None
    ativo: Optional[bool] = None


class ProdutoResponse(BaseModel):
    """Schema de resposta com dados do produto"""
    id: UUID
    nome: str
    categoria: Optional[str]
    preco_padrao: float
    ativo: bool
    created_at: datetime
    updated_at: datetime


# ==================== ENDPOINTS ====================

@router.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos(
    apenas_ativos: bool = Query(True, description="Filtrar apenas produtos ativos"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria")
):
    """
    Lista todos os produtos do catálogo.
    Por padrão, retorna apenas produtos ativos.
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table("produtos").select("*")
        
        if apenas_ativos:
            query = query.eq("ativo", True)
        
        if categoria:
            query = query.eq("categoria", categoria)
        
        response = query.order("nome").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: str):
    """Obtém detalhes de um produto específico"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("produtos")\
            .select("*")\
            .eq("id", produto_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")


@router.post("/produtos", response_model=ProdutoResponse, status_code=201)
async def criar_produto(produto: ProdutoCreate):
    """Cria um novo produto no catálogo"""
    try:
        supabase = get_supabase_client()
        
        # Verificar se já existe produto com esse nome
        check = supabase.table("produtos")\
            .select("id")\
            .eq("nome", produto.nome)\
            .execute()
        
        if check.data:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um produto com o nome '{produto.nome}'"
            )
        
        response = supabase.table("produtos")\
            .insert({
                "nome": produto.nome,
                "categoria": produto.categoria,
                "preco_padrao": float(produto.preco_padrao)
            })\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao criar produto")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")


@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(produto_id: str, produto: ProdutoUpdate):
    """Atualiza um produto existente"""
    try:
        supabase = get_supabase_client()
        
        update_data = {}
        if produto.nome is not None:
            update_data["nome"] = produto.nome
        if produto.categoria is not None:
            update_data["categoria"] = produto.categoria
        if produto.preco_padrao is not None:
            update_data["preco_padrao"] = float(produto.preco_padrao)
        if produto.ativo is not None:
            update_data["ativo"] = produto.ativo
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        response = supabase.table("produtos")\
            .update(update_data)\
            .eq("id", produto_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")


@router.delete("/produtos/{produto_id}", status_code=204)
async def desativar_produto(produto_id: str):
    """
    Desativa um produto (soft delete).
    O produto não é deletado, apenas marcado como inativo.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("produtos")\
            .update({"ativo": False})\
            .eq("id", produto_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao desativar produto: {str(e)}")


@router.get("/produtos/categorias/listar")
async def listar_categorias():
    """Lista todas as categorias de produtos cadastradas"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("produtos")\
            .select("categoria")\
            .neq("categoria", None)\
            .execute()
        
        categorias = list(set(p["categoria"] for p in response.data if p.get("categoria")))
        return sorted(categorias)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar categorias: {str(e)}")