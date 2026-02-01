import { DollarSign, ShoppingBag } from 'lucide-react'

function DailyTotal({ total, loading, quantidadeItens }) {
  return (
    <div className="card bg-gradient-to-r from-green-500 to-emerald-600 text-white">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <DollarSign className="w-5 h-5" />
            <span className="text-sm font-medium opacity-90">Total do Dia</span>
          </div>
          
          {loading ? (
            <div className="h-10 w-32 bg-white/20 rounded animate-pulse"></div>
          ) : (
            <p className="text-3xl md:text-4xl font-bold">
              R$ {total.toFixed(2).replace('.', ',')}
            </p>
          )}
        </div>

        <div className="text-right">
          <div className="flex items-center gap-2 justify-end mb-1">
            <ShoppingBag className="w-5 h-5" />
            <span className="text-sm font-medium opacity-90">Itens</span>
          </div>
          <p className="text-3xl md:text-4xl font-bold">
            {quantidadeItens}
          </p>
        </div>
      </div>
    </div>
  )
}

export default DailyTotal