import { Menu, X, Calendar, TrendingUp } from 'lucide-react'
import { useState } from 'react'

function MenuToggle({ viewAtual, onChangeView }) {
  const [menuAberto, setMenuAberto] = useState(false)

  const opcoes = [
    { id: 'diario', label: 'Controle Diário', icon: Calendar },
    { id: 'mensal', label: 'Controle Mensal', icon: TrendingUp }
  ]

  const handleSelectView = (viewId) => {
    onChangeView(viewId)
    setMenuAberto(false)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setMenuAberto(!menuAberto)}
        className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
        aria-label="Menu"
      >
        {menuAberto ? (
          <X className="w-6 h-6" />
        ) : (
          <Menu className="w-6 h-6" />
        )}
      </button>

      {menuAberto && (
        <>
          {/* Overlay para fechar ao clicar fora */}
          <div 
            className="fixed inset-0 z-40"
            onClick={() => setMenuAberto(false)}
          />
          
          {/* Menu dropdown */}
          <div className="absolute right-0 top-full mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden">
            {opcoes.map((opcao) => {
              const Icon = opcao.icon
              const isAtivo = viewAtual === opcao.id
              
              return (
                <button
                  key={opcao.id}
                  onClick={() => handleSelectView(opcao.id)}
                  className={`
                    w-full px-4 py-3 flex items-center gap-3 text-left transition-colors
                    ${isAtivo 
                      ? 'bg-primary-50 text-primary-700 font-medium' 
                      : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{opcao.label}</span>
                  {isAtivo && (
                    <span className="ml-auto w-2 h-2 bg-primary-600 rounded-full"></span>
                  )}
                </button>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}

export default MenuToggle