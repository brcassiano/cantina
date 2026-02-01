import { useState, useEffect } from 'react'
import { DollarSign, Calendar, TrendingUp } from 'lucide-react'

function ControleMensal() {
  const [mesAtual, setMesAtual] = useState('')
  const [vendasDoMes, setVendasDoMes] = useState([])
  const [totalMes, setTotalMes] = useState(0)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const hoje = new Date()
    const mesAno = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}`
    setMesAtual(mesAno)
    carregarVendasMes(mesAno)
  }, [])

  const carregarVendasMes = (mesAno) => {
    setLoading(true)
    
    setTimeout(() => {
      const todasVendas = JSON.parse(localStorage.getItem('vendas') || '[]')
      
      const vendasFiltradas = todasVendas.filter(v => {
        return v.data.startsWith(mesAno)
      })
      
      vendasFiltradas.sort((a, b) => new Date(b.data) - new Date(a.data))
      
      setVendasDoMes(vendasFiltradas)
      
      const total = vendasFiltradas.reduce((acc, v) => acc + parseFloat(v.preco), 0)
      setTotalMes(total)
      
      setLoading(false)
    }, 300)
  }

  const formatarMesExibicao = (mesAno) => {
    const [ano, mes] = mesAno.split('-')
    const date = new Date(ano, parseInt(mes) - 1)
    return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })
  }

  const agruparPorData = () => {
    const grupos = {}
    
    vendasDoMes.forEach(venda => {
      if (!grupos[venda.data]) {
        grupos[venda.data] = []
      }
      grupos[venda.data].push(venda)
    })
    
    return grupos
  }

  const handleMesChange = (e) => {
    const novoMes = e.target.value
    setMesAtual(novoMes)
    carregarVendasMes(novoMes)
  }

  // Mês/ano máximo permitido (hoje)
  const mesAnoAtual = (() => {
    const hoje = new Date()
    return `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}`
  })()

  const vendasAgrupadas = agruparPorData()
  const datasOrdenadas = Object.keys(vendasAgrupadas).sort().reverse()

  return (
    <div className="space-y-4">
      {/* Seletor de Mês */}
      <div className="card">
        <div className="flex items-center gap-2 mb-2">
          <Calendar className="w-5 h-5 text-primary-600" />
          <label htmlFor="month-input" className="text-sm font-medium text-gray-600">
            Selecionar mês
          </label>
        </div>
        
        <input
          id="month-input"
          type="month"
          value={mesAtual}
          onChange={handleMesChange}
          max={mesAnoAtual}
          className="input-field"
        />
        
        <p className="text-xs text-gray-500 mt-2 capitalize">
          {formatarMesExibicao(mesAtual)}
        </p>
      </div>

      {/* Total do Mês */}
      <div className="card bg-gradient-to-r from-purple-500 to-indigo-600 text-white">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-5 h-5" />
              <span className="text-sm font-medium opacity-90">Total do Mês</span>
            </div>
            
            {loading ? (
              <div className="h-10 w-32 bg-white/20 rounded animate-pulse"></div>
            ) : (
              <p className="text-3xl md:text-4xl font-bold">
                R$ {totalMes.toFixed(2).replace('.', ',')}
              </p>
            )}
          </div>

          <div className="text-right">
            <div className="flex items-center gap-2 justify-end mb-1">
              <DollarSign className="w-5 h-5" />
              <span className="text-sm font-medium opacity-90">Vendas</span>
            </div>
            <p className="text-3xl md:text-4xl font-bold">
              {vendasDoMes.length}
            </p>
          </div>
        </div>
      </div>

      {/* Lista de Vendas por Data */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-800">
          Histórico de Vendas
        </h2>

        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            ))}
          </div>
        ) : vendasDoMes.length === 0 ? (
          <div className="card text-center py-12">
            <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">Nenhuma venda neste mês</p>
            <p className="text-gray-400 text-sm mt-1">
              Selecione outro mês ou adicione vendas
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {datasOrdenadas.map(data => {
              const vendasDoDia = vendasAgrupadas[data]
              const totalDia = vendasDoDia.reduce((acc, v) => acc + parseFloat(v.preco), 0)
              
              const dataFormatada = new Date(data + 'T00:00:00').toLocaleDateString('pt-BR', {
                weekday: 'short',
                day: '2-digit',
                month: 'short',
                year: 'numeric'
              })

              return (
                <div key={data} className="card">
                  <div className="flex items-center justify-between mb-3 pb-3 border-b border-gray-200">
                    <h3 className="font-semibold text-gray-800 capitalize">
                      {dataFormatada}
                    </h3>
                    <span className="text-lg font-bold text-green-600">
                      R$ {totalDia.toFixed(2).replace('.', ',')}
                    </span>
                  </div>

                  <div className="space-y-2">
                    {vendasDoDia.map(venda => (
                      <div 
                        key={venda.id} 
                        className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-800 truncate">
                            {venda.item}
                          </p>
                          <p className="text-xs text-gray-500">
                            {new Date(venda.createdAt).toLocaleTimeString('pt-BR', { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </p>
                        </div>
                        <span className="text-green-600 font-semibold ml-3 whitespace-nowrap">
                          R$ {parseFloat(venda.preco).toFixed(2).replace('.', ',')}
                        </span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-3 pt-3 border-t border-gray-200 flex justify-between text-sm">
                    <span className="text-gray-600">
                      {vendasDoDia.length} {vendasDoDia.length === 1 ? 'item' : 'itens'}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default ControleMensal