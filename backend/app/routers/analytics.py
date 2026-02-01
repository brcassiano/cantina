from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from collections import defaultdict, Counter
from ..database import get_supabase_client

router = APIRouter()


# ==================== SCHEMAS ====================

class ItemMaisVendido(BaseModel):
    item: str
    quantidade_vendida: int
    faturamento_total: float
    percentual: float


class FaturamentoDiario(BaseModel):
    data: date
    total: float
    quantidade_vendas: int


class VendasPorCategoria(BaseModel):
    categoria: str
    quantidade_vendas: int
    faturamento_total: float
    percentual: float


class ComparativoMensal(BaseModel):
    mes: str
    total_faturado: float
    quantidade_vendas: int
    ticket_medio: float


class EstatisticasGerais(BaseModel):
    total_faturado: float
    quantidade_vendas: int
    ticket_medio: float
    item_mais_vendido: Optional[str]
    melhor_dia: Optional[date]


# ==================== ENDPOINTS ====================

@router.get("/analytics/mais-vendidos", response_model=List[ItemMaisVendido])
async def itens_mais_vendidos(
    data_inicio: date = Query(..., description="Data inicial do período"),
    data_fim: date = Query(..., description="Data final do período"),
    limit: int = Query(10, le=50, description="Quantidade de itens no ranking")
):
    """
    Ranking dos itens mais vendidos em um período.
    Retorna nome, quantidade, faturamento e percentual.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("item, preco, quantidade")\
            .gte("data", data_inicio.isoformat())\
            .lte("data", data_fim.isoformat())\
            .execute()
        
        vendas = response.data
        
        if not vendas:
            return []
        
        # Agrupar por item
        itens_stats = defaultdict(lambda: {"quantidade": 0, "faturamento": 0.0})
        
        for v in vendas:
            item = v["item"]
            qtd = v.get("quantidade", 1)
            preco = float(v["preco"])
            
            itens_stats[item]["quantidade"] += qtd
            itens_stats[item]["faturamento"] += preco * qtd
        
        # Calcular total para percentuais
        total_vendas = sum(s["quantidade"] for s in itens_stats.values())
        
        # Ordenar e limitar
        ranking = sorted(
            itens_stats.items(),
            key=lambda x: x[1]["quantidade"],
            reverse=True
        )[:limit]
        
        return [
            {
                "item": item,
                "quantidade_vendida": stats["quantidade"],
                "faturamento_total": round(stats["faturamento"], 2),
                "percentual": round(stats["quantidade"] / total_vendas * 100, 2) if total_vendas > 0 else 0
            }
            for item, stats in ranking
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular ranking: {str(e)}")


@router.get("/analytics/faturamento-diario", response_model=List[FaturamentoDiario])
async def faturamento_diario(
    mes_ano: str = Query(..., description="Mês no formato YYYY-MM")
):
    """
    Faturamento dia a dia de um mês específico.
    Ideal para gráficos de linha.
    """
    try:
        datetime.strptime(mes_ano, "%Y-%m")
        
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("data, preco, quantidade")\
            .gte("data", f"{mes_ano}-01")\
            .lt("data", f"{mes_ano}-32")\
            .order("data")\
            .execute()
        
        # Agrupar por data
        por_dia = defaultdict(lambda: {"total": 0.0, "quantidade": 0})
        
        for v in response.data:
            data = v["data"]
            qtd = v.get("quantidade", 1)
            preco = float(v["preco"])
            
            por_dia[data]["total"] += preco * qtd
            por_dia[data]["quantidade"] += 1
        
        return [
            {
                "data": data,
                "total": round(stats["total"], 2),
                "quantidade_vendas": stats["quantidade"]
            }
            for data, stats in sorted(por_dia.items())
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato inválido. Use YYYY-MM")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular faturamento: {str(e)}")


@router.get("/analytics/vendas-por-categoria", response_model=List[VendasPorCategoria])
async def vendas_por_categoria(
    data_inicio: date = Query(...),
    data_fim: date = Query(...)
):
    """
    Distribuição de vendas por categoria de produto.
    Ideal para gráfico de pizza.
    """
    try:
        supabase = get_supabase_client()
        
        # Buscar vendas com JOIN em produtos (via view)
        response = supabase.from_("vendas_completas")\
            .select("categoria, preco, quantidade")\
            .gte("data", data_inicio.isoformat())\
            .lte("data", data_fim.isoformat())\
            .execute()
        
        # Agrupar por categoria
        por_categoria = defaultdict(lambda: {"quantidade": 0, "faturamento": 0.0})
        
        for v in response.data:
            categoria = v.get("categoria") or "Sem Categoria"
            qtd = v.get("quantidade", 1)
            preco = float(v["preco"])
            
            por_categoria[categoria]["quantidade"] += 1
            por_categoria[categoria]["faturamento"] += preco * qtd
        
        # Calcular total para percentuais
        total_faturamento = sum(s["faturamento"] for s in por_categoria.values())
        
        return [
            {
                "categoria": cat,
                "quantidade_vendas": stats["quantidade"],
                "faturamento_total": round(stats["faturamento"], 2),
                "percentual": round(stats["faturamento"] / total_faturamento * 100, 2) if total_faturamento > 0 else 0
            }
            for cat, stats in sorted(por_categoria.items(), key=lambda x: x[1]["faturamento"], reverse=True)
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular vendas por categoria: {str(e)}")


@router.get("/analytics/comparativo-mensal", response_model=List[ComparativoMensal])
async def comparativo_mensal(
    quantidade_meses: int = Query(6, ge=1, le=24, description="Quantos meses retornar")
):
    """
    Comparativo de faturamento dos últimos N meses.
    Ideal para gráfico de barras.
    """
    try:
        supabase = get_supabase_client()
        
        # Calcular data de início
        hoje = date.today()
        data_inicio = hoje - timedelta(days=quantidade_meses * 31)
        
        response = supabase.table("vendas")\
            .select("data, preco, quantidade")\
            .gte("data", data_inicio.isoformat())\
            .order("data")\
            .execute()
        
        # Agrupar por mês
        por_mes = defaultdict(lambda: {"total": 0.0, "quantidade": 0})
        
        for v in response.data:
            mes = v["data"][:7]  # YYYY-MM
            qtd = v.get("quantidade", 1)
            preco = float(v["preco"])
            
            por_mes[mes]["total"] += preco * qtd
            por_mes[mes]["quantidade"] += 1
        
        return [
            {
                "mes": mes,
                "total_faturado": round(stats["total"], 2),
                "quantidade_vendas": stats["quantidade"],
                "ticket_medio": round(stats["total"] / stats["quantidade"], 2) if stats["quantidade"] > 0 else 0
            }
            for mes, stats in sorted(por_mes.items())[-quantidade_meses:]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular comparativo: {str(e)}")


@router.get("/analytics/estatisticas-gerais", response_model=EstatisticasGerais)
async def estatisticas_gerais(
    data_inicio: date = Query(...),
    data_fim: date = Query(...)
):
    """
    Estatísticas gerais de um período.
    Resumo executivo para dashboard.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("data, item, preco, quantidade")\
            .gte("data", data_inicio.isoformat())\
            .lte("data", data_fim.isoformat())\
            .execute()
        
        vendas = response.data
        
        if not vendas:
            return {
                "total_faturado": 0.0,
                "quantidade_vendas": 0,
                "ticket_medio": 0.0,
                "item_mais_vendido": None,
                "melhor_dia": None
            }
        
        # Calcular métricas
        total_faturado = sum(float(v["preco"]) * v.get("quantidade", 1) for v in vendas)
        quantidade_vendas = len(vendas)
        ticket_medio = total_faturado / quantidade_vendas
        
        # Item mais vendido
        itens = [v["item"] for v in vendas]
        item_mais_vendido = Counter(itens).most_common(1)[0][0] if itens else None
        
        # Melhor dia
        faturamento_por_dia = defaultdict(float)
        for v in vendas:
            faturamento_por_dia[v["data"]] += float(v["preco"]) * v.get("quantidade", 1)
        
        melhor_dia = max(faturamento_por_dia.items(), key=lambda x: x[1])[0] if faturamento_por_dia else None
        
        return {
            "total_faturado": round(total_faturado, 2),
            "quantidade_vendas": quantidade_vendas,
            "ticket_medio": round(ticket_medio, 2),
            "item_mais_vendido": item_mais_vendido,
            "melhor_dia": melhor_dia
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular estatísticas: {str(e)}")


@router.get("/analytics/tendencia-semanal")
async def tendencia_semanal(
    data_inicio: date = Query(...),
    data_fim: date = Query(...)
):
    """
    Faturamento por dia da semana (seg, ter, qua...).
    Identifica padrões de vendas.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("vendas")\
            .select("data, preco, quantidade")\
            .gte("data", data_inicio.isoformat())\
            .lte("data", data_fim.isoformat())\
            .execute()
        
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        por_dia_semana = defaultdict(lambda: {"total": 0.0, "ocorrencias": 0})
        
        for v in response.data:
            data_obj = datetime.strptime(v["data"], "%Y-%m-%d")
            dia_semana = dias_semana[data_obj.weekday()]
            qtd = v.get("quantidade", 1)
            preco = float(v["preco"])
            
            por_dia_semana[dia_semana]["total"] += preco * qtd
            por_dia_semana[dia_semana]["ocorrencias"] += 1
        
        resultado = []
        for dia in dias_semana:
            stats = por_dia_semana[dia]
            media = stats["total"] / stats["ocorrencias"] if stats["ocorrencias"] > 0 else 0
            resultado.append({
                "dia_semana": dia,
                "total": round(stats["total"], 2),
                "media_diaria": round(media, 2),
                "quantidade_dias": stats["ocorrencias"]
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular tendência: {str(e)}")