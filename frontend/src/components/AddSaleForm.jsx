import { useState } from 'react'
import { Plus } from 'lucide-react'

function AddSaleForm({ onSubmit }) {
  const [item, setItem] = useState('')
  const [preco, setPreco] = useState('')
  const [isAdding, setIsAdding] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!item.trim() || !preco) {
      alert('Por favor, preencha todos os campos')
      return
    }

    const precoNumerico = parseFloat(preco)
    if (isNaN(precoNumerico) || precoNumerico <= 0) {
      alert('Preço inválido')
      return
    }

    setIsAdding(true)
    
    // Simular delay
    setTimeout(() => {
      onSubmit({ item: item.trim(), preco: precoNumerico })
      setItem('')
      setPreco('')
      setIsAdding(false)
    }, 200)
  }

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
        <Plus className="w-5 h-5 text-primary-600" />
        Adicionar Venda
      </h2>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label htmlFor="item" className="block text-sm font-medium text-gray-700 mb-1">
            Item vendido
          </label>
          <input
            id="item"
            type="text"
            placeholder="Ex: Suco de laranja, Coxinha..."
            value={item}
            onChange={(e) => setItem(e.target.value)}
            className="input-field"
            disabled={isAdding}
          />
        </div>

        <div>
          <label htmlFor="preco" className="block text-sm font-medium text-gray-700 mb-1">
            Preço (R$)
          </label>
          <input
            id="preco"
            type="number"
            step="0.01"
            min="0"
            placeholder="0,00"
            value={preco}
            onChange={(e) => setPreco(e.target.value)}
            className="input-field"
            disabled={isAdding}
          />
        </div>

        <button
          type="submit"
          disabled={isAdding}
          className="btn-primary w-full py-3 text-base font-semibold flex items-center justify-center gap-2"
        >
          {isAdding ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Adicionando...
            </>
          ) : (
            <>
              <Plus className="w-5 h-5" />
              Adicionar Venda
            </>
          )}
        </button>
      </form>
    </div>
  )
}

export default AddSaleForm