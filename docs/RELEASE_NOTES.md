# Release Notes — Frontend

## Deploy em Vercel

1. **Conectar repositório**
   - Acesse [vercel.com](https://vercel.com) e importe o repositório
   - Defina o **Root Directory** como `frontend`

2. **Variáveis de ambiente**
   - `NEXT_PUBLIC_API_URL` — URL do backend (ex: `https://api.exemplo.com` ou `http://localhost:8000` em dev)

3. **Build**
   - Build Command: `npm run build` (padrão)
   - Output Directory: `.next` (padrão)
   - Install Command: `npm install` (padrão)

4. **CORS**
   - O backend deve permitir requisições do domínio Vercel (`*.vercel.app` ou domínio customizado)

## Checklist de release

- [ ] Backend rodando e acessível
- [ ] `NEXT_PUBLIC_API_URL` configurada no Vercel
- [ ] `npm run build` passa localmente
- [ ] `npm run test` passa
- [ ] `npm run test:e2e` passa (opcional)
- [ ] Deploy de preview verificado antes do merge

## v0.1.0 (frontend inicial)

- Next.js + MUI
- Páginas: início, criar job, lista de jobs, detalhe do job
- Integração com API: postOptimize, getJob, getJobs, getRoutes, postInstructions
- Componentes: Layout, JobCard, MapPreview
- Testes: Jest + RTL, jest-axe, Playwright E2E
- CI: `.github/workflows/frontend-ci.yml`
