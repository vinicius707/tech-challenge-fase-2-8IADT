# Componentes

## Layout

`components/Layout.js` — layout global com AppBar, Toolbar e Container. Inclui links de navegação (Início, Criar Job, Jobs). Usado em `_app.js` para envolver todas as páginas.

## JobCard

`components/JobCard.js` — card com resumo do job: ID abreviado, status (chip colorido) e botão "Ver detalhes". Recebe `job` com `job_id` e `status`.

```jsx
<JobCard job={{ job_id: 'abc-123', status: 'finished' }} />
```

## MapPreview

`components/MapPreview.js` — exibe mapa de rotas via iframe ou mensagem fallback. Recebe `mapUrl`; se `null`, mostra alert informando que o mapa não está disponível.

```jsx
<MapPreview mapUrl={mapUrl} />
<MapPreview mapUrl={null} />  // fallback
```

## Responsividade

O layout usa breakpoints MUI (xs, sm, md, lg). Em mobile, os JobCards ocupam 100% da largura e a navegação quebra linha. O formulário de criação é full-width em telas pequenas.
