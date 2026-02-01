import SaleItem from './SaleItem'
import { ShoppingCart } from 'lucide-react'

function SalesList({ vendas, loading, onDelete, onEdit }) {
  if (loading) {
    return (
      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-800">Vendas do Dia</h2>
        {[1, 2, 3].map((i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          </div>
        ))}
      </div>
    )
  }

  if (vendas.length === 0) {
    return (
      <div className="card text-center py-12">
        <ShoppingCart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500 font-medium">Nenhuma venda registrada</p>
        <p className="text-gray-400 text-sm mt-1">
          Adicione a primeira venda do dia acima
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold text-gray-800 flex items-center justify-between">
        <span>Vendas do Dia</span>
        <span className="text-sm text-gray-500 font-normal">
          {vendas.length} {vendas.length === 1 ? 'item' : 'itens'}
        </span>
      </h2>

      <div className="space-y-2">
        {vendas.map((venda) => (
          <SaleItem
            key={venda.id}
            venda={venda}
            onDelete={onDelete}
            onEdit={onEdit}
          />
        ))}
      </div>
    </div>
  )
}

export default SalesList