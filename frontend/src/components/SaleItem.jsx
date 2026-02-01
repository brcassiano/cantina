import { useState } from 'react'
import { Trash2, Edit2, Check, X } from 'lucide-react'

function SaleItem({ venda, onDelete, onEdit }) {
  const [editando, setEditando] = useState(false)
  const [itemEditado, setItemEditado] = useState(venda.item)
  const [quantidadeEditada, setQuantidadeEditada] = useState(venda.quantidade || 1)
  const [precoEditado, setPrecoEditado] = useState(venda.preco)

  const handleSalvar = () => {
    if (!itemEditado.trim() || !precoEditado || quantidadeEditada < 1) {
      alert('Campos inválidos')
      return
    }

    const precoNum = parseFloat(precoEditado)
    const qtd = parseInt(quantidadeEditada)

    onEdit(venda.id, {
      item: itemEditado.trim(),
      quantidade: qtd,
      preco: precoNum,
      total: qtd * precoNum
    })
    setEditando(false)
  }

  const handleCancelar = () => {
    setItemEditado(venda.item)
    setQuantidadeEditada(venda.quantidade || 1)
    setPrecoEditado(venda.preco)
    setEditando(false)
  }

  if (editando) {
    return (
      <div className="card border-primary-300">
        <div className="space-y-2">
          <input
            type="text"
            value={itemEditado}
            onChange={(e) => setItemEditado(e.target.value)}
            className="input-field text-sm py-2"
            placeholder="Nome do item"
          />
          
          <input
            type="number"
            min="1"
            value={quantidadeEditada}
            onChange={(e) => setQuantidadeEditada(e.target.value)}
            className="input-field text-sm py-2"
            placeholder="Quantidade"
          />
          
          <input
            type="number"
            step="0.01"
            min="0"
            value={precoEditado}
            onChange={(e) => setPrecoEditado(e.target.value)}
            className="input-field text-sm py-2"
            placeholder="Preço unitário"
          />
          
          <div className="flex gap-2">
            <button
              onClick={handleSalvar}
              className="flex-1 bg-green-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-700 flex items-center justify-center gap-1"
            >
              <Check className="w-4 h-4" />
              Salvar
            </button>
            <button
              onClick={handleCancelar}
              className="flex-1 btn-secondary text-sm py-2 flex items-center justify-center gap-1"
            >
              <X className="w-4 h-4" />
              Cancelar
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-gray-800 truncate">
            {venda.item}
          </h3>
          <p className="text-xs text-gray-500 mt-0.5">
            {venda.quantidade || 1}x R$ {parseFloat(venda.preco).toFixed(2).replace('.', ',')} • {' '}
            {new Date(venda.createdAt).toLocaleTimeString('pt-BR', { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <p className="text-lg font-bold text-green-600 whitespace-nowrap">
            R$ {parseFloat(venda.total || venda.preco).toFixed(2).replace('.', ',')}
          </p>

          <div className="flex gap-1">
            <button
              onClick={() => setEditando(true)}
              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              aria-label="Editar"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => {
                if (confirm('Confirma exclusão?')) {
                  onDelete(venda.id)
                }
              }}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              aria-label="Excluir"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SaleItem