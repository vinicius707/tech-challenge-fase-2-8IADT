# Tech Challenge — Frontend (Next.js + MUI)

Interface web para o Projeto 2 (Otimização de Rotas Médicas). Permite criar jobs de otimização, listar jobs, visualizar artefatos e gerar instruções via LLM.

## Pré-requisitos

- Node.js 18+
- API backend rodando (ex.: `uvicorn src.api.app:app --port 8000`)

## Quickstart

```bash
npm install
npm run dev
```

Acesse http://localhost:3000

## Scripts

- `npm run dev` — servidor de desenvolvimento
- `npm run build` — build de produção
- `npm run start` — rodar build de produção
- `npm run test` — testes unitários (Jest + React Testing Library)
- `npm run test:e2e` — testes E2E (Playwright)
- `npm run lint` — lint com ESLint

## Estrutura

- `pages/` — rotas Next.js (Pages Router)
- `components/` — componentes MUI reutilizáveis
- `lib/api.js` — wrappers para a API backend

## Deploy (Vercel)

1. Conecte o repositório ao Vercel
2. Defina o diretório raiz como `frontend`
3. Configure a variável `NEXT_PUBLIC_API_URL` com a URL do backend
4. Build Command: `npm run build`
5. Output Directory: `.next` (padrão)

## Documentação

- [Componentes](docs/components.md)
- [API lib](docs/api.md)
