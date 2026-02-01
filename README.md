# Cantina Escolar - Sistema de Gestão de Vendas

Sistema web mobile-first para controle de vendas de cantina escolar.

## Tecnologias

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Banco de Dados**: Supabase (PostgreSQL)
- **Deploy**: Docker + Easypanel

## Estrutura do Projeto

CANTINA/
├── cantina/ # Frontend React
├── backend/ # API FastAPI
└── README.md

text

## Configuração Local (Desenvolvimento)

### Frontend
```bash
cd cantina
npm install
npm run dev
Backend
bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure suas credenciais
uvicorn app.main:app --reload
Deploy com Docker
Backend
bash
cd backend
docker build -t cantina-backend .
docker run -p 8000:8000 --env-file .env cantina-backend
Variáveis de Ambiente
Crie um arquivo .env no backend com:

text
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_service_role_key
ENVIRONMENT=production
Endpoints API
Documentação: http://localhost:8000/docs

Vendas: /api/v1/vendas

Produtos: /api/v1/produtos

Analytics: /api/v1/analytics

Licença
Privado