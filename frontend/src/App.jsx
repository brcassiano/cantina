import { useState, useEffect } from 'react'
import DateSelector from './components/DateSelector'
import DailyTotal from './components/DailyTotal'
import AddSaleForm from './components/AddSaleForm'
import SalesList from './components/SalesList'
import ControleMensal from './components/ControleMensal'
import MenuToggle from './components/MenuToggle'

function App() {
  const [viewAtual, setViewAtual] = useState('diario')
  const [dataSelecionada, setDataSelecionada] = useState(
    new Date().toISOString().split('T')[0]
  )
  const [vendas, setVendas] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (viewAtual === 'diario') {
      carregarVendas(dataSelecionada)
    }
  }, [dataSelecionada, viewAtual])

  const carregarVendas = (data) => {
    setLoading(true)
    
    setTimeout(() => {
      const todasVendas = JSON.parse(localStorage.getItem('vendas') || '[]')
      const vendasDoDia = todasVendas.filter(v => v.data === data)
      setVendas(vendasDoDia)
      setLoading(false)
    }, 300)
  }

  const adicionarVenda = (novaVenda) => {
    const venda = {
      id: Date.now().toString(),
      data: dataSelecionada,
      ...novaVenda,
      createdAt: new Date().toISOString()
    }

    const todasVendas = JSON.parse(localStorage.getItem('vendas') || '[]')
    todasVendas.push(venda)
    localStorage.setItem('vendas', JSON.stringify(todasVendas))

    setVendas([...vendas, venda])
  }

  const deletarVenda = (id) => {
    const todasVendas = JSON.parse(localStorage.getItem('vendas') || '[]')
    const vendasAtualizadas = todasVendas.filter(v => v.id !== id)
    localStorage.setItem('vendas', JSON.stringify(vendasAtualizadas))

    setVendas(vendas.filter(v => v.id !== id))
  }

  const editarVenda = (id, vendaEditada) => {
    const todasVendas = JSON.parse(localStorage.getItem('vendas') || '[]')
    const vendasAtualizadas = todasVendas.map(v => 
      v.id === id ? { ...v, ...vendaEditada } : v
    )
    localStorage.setItem('vendas', JSON.stringify(vendasAtualizadas))

    setVendas(vendas.map(v => 
      v.id === id ? { ...v, ...vendaEditada } : v
    ))
  }

  const calcularTotal = () => {
    return vendas.reduce((acc, venda) => {
      const total = venda.total || (venda.preco * (venda.quantidade || 1))
      return acc + parseFloat(total)
    }, 0)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 pb-8">
      <div className="bg-primary-600 text-white shadow-lg">
        <div className="max-w-2xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold flex items-center gap-2">
                <span className="text-3xl">🏫</span>
                Cantina Escolar
              </h1>
              <p className="text-blue-100 text-sm mt-1">
                {viewAtual === 'diario' ? 'Controle de vendas diárias' : 'Resumo mensal'}
              </p>
            </div>
            
            <MenuToggle viewAtual={viewAtual} onChangeView={setViewAtual} />
          </div>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
        {viewAtual === 'diario' ? (
          <>
            <DateSelector 
              dataSelecionada={dataSelecionada}
              onChange={setDataSelecionada}
            />
            
            <DailyTotal 
              total={calcularTotal()} 
              loading={loading}
              quantidadeItens={vendas.length}
            />
            
            <AddSaleForm onSubmit={adicionarVenda} />
            
            <SalesList 
              vendas={vendas}
              loading={loading}
              onDelete={deletarVenda}
              onEdit={editarVenda}
            />
          </>
        ) : (
          <ControleMensal />
        )}
      </div>
    </div>
  )
}

export default App