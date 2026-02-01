import { Calendar } from 'lucide-react'

function DateSelector({ dataSelecionada, onChange }) {
  const formatarDataExibicao = (data) => {
    const date = new Date(data + 'T00:00:00')
    return date.toLocaleDateString('pt-BR', { 
      weekday: 'long', 
      day: '2-digit', 
      month: 'long',
      year: 'numeric'
    })
  }

  const irParaHoje = () => {
    onChange(new Date().toISOString().split('T')[0])
  }

  const hoje = new Date().toISOString().split('T')[0]
  const ehHoje = dataSelecionada === hoje

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-2">
        <Calendar className="w-5 h-5 text-primary-600" />
        <label htmlFor="date-input" className="text-sm font-medium text-gray-600">
          Data selecionada
        </label>
      </div>
      
      <input
        id="date-input"
        type="date"
        value={dataSelecionada}
        onChange={(e) => onChange(e.target.value)}
        max={hoje}
        className="input-field"
      />
      
      <p className="text-xs text-gray-500 mt-2 capitalize">
        {formatarDataExibicao(dataSelecionada)}
      </p>

      {!ehHoje && (
        <button
          onClick={irParaHoje}
          className="w-full mt-3 text-primary-600 text-sm font-medium hover:underline"
        >
          Voltar para hoje
        </button>
      )}
    </div>
  )
}

export default DateSelector