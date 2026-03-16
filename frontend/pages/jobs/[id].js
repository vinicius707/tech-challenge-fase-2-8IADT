import * as React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import CircularProgress from '@mui/material/CircularProgress'
import LinearProgress from '@mui/material/LinearProgress'
import Alert from '@mui/material/Alert'
import Chip from '@mui/material/Chip'
import Paper from '@mui/material/Paper'
import { getJob, getRoutes, postInstructions, askJobQuestion } from '../../lib/api'
import MapPreview from '../../components/MapPreview'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function JobDetail() {
  const router = useRouter()
  const { id } = router.query
  const [instructionPath, setInstructionPath] = React.useState(null)
  const [instructionLoading, setInstructionLoading] = React.useState(false)
  const [instructionError, setInstructionError] = React.useState(null)
  const [question, setQuestion] = React.useState('')
  const [answer, setAnswer] = React.useState(null)
  const [askLoading, setAskLoading] = React.useState(false)
  const [askError, setAskError] = React.useState(null)

  const { data: job, error: jobError } = useSWR(
    id ? `job-${id}` : null,
    () => getJob(id),
    { refreshInterval: 2000 }
  )

  const { data: routes } = useSWR(
    id && job?.status === 'finished' ? `routes-${id}` : null,
    () => getRoutes(id),
    { refreshInterval: 0 }
  )

  const mapUrl =
    job?.status === 'finished' && job?.out_dir
      ? `${API_BASE}/artifacts/jobs/${id}/route_map.html`
      : null

  const historyUrl =
    job?.status === 'finished' && job?.out_dir
      ? `${API_BASE}/artifacts/jobs/${id}/history.csv`
      : null

  const handleExport = () => {
    if (mapUrl) window.open(mapUrl, '_blank')
  }

  const handleAsk = async () => {
    if (!id || !question.trim()) return
    setAskError(null)
    setAnswer(null)
    setAskLoading(true)
    try {
      const res = await askJobQuestion(id, question.trim())
      setAnswer(res.answer)
    } catch (err) {
      setAskError(err.body?.detail || err.message || 'Erro ao perguntar')
    } finally {
      setAskLoading(false)
    }
  }

  const handleGenerateInstructions = async () => {
    if (!id) return
    setInstructionError(null)
    setInstructionLoading(true)
    try {
      const res = await postInstructions(id)
      setInstructionPath(res.instruction)
    } catch (err) {
      setInstructionError(err.body?.detail || err.message || 'Erro ao gerar instruções')
    } finally {
      setInstructionLoading(false)
    }
  }

  if (!id) return null
  if (jobError) {
    return <Alert severity="error">Planejamento não encontrado.</Alert>
  }
  if (!job) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Planejamento {id.slice(0, 8)}
      </Typography>
      <Chip
        label={{ queued: 'Na fila', running: 'Em execução', finished: 'Concluído', failed: 'Falhou' }[job.status] || job.status}
        color={job.status === 'finished' ? 'success' : job.status === 'failed' ? 'error' : 'default'}
        sx={{ mb: 2 }}
      />

      {(job.status === 'running' || job.status === 'queued') && (
        <Box sx={{ width: '100%', mb: 2 }}>
          <LinearProgress
            variant={job.progress?.total ? 'determinate' : 'indeterminate'}
            value={job.progress?.total ? Math.round((job.progress.current / job.progress.total) * 100) : 0}
            sx={{ height: 8, borderRadius: 1 }}
          />
          {job.progress?.total && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
              Planejando rota… {job.progress.current} / {job.progress.total}
            </Typography>
          )}
        </Box>
      )}

      {job.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {job.error}
        </Alert>
      )}

      {historyUrl && (
        <Box sx={{ mb: 2 }}>
          <Button href={historyUrl} target="_blank" rel="noopener" component="a">
            Baixar histórico (CSV)
          </Button>
        </Box>
      )}

      {job.status === 'finished' && (
        <>
          <Box sx={{ mb: 2 }}>
            <Button variant="contained" onClick={handleExport} sx={{ mr: 2 }}>
              Abrir mapa
            </Button>
            <Button
              variant="outlined"
              onClick={handleGenerateInstructions}
              disabled={instructionLoading}
            >
              {instructionLoading ? 'Gerando…' : 'Gerar resumo'}
            </Button>
          </Box>
          {instructionError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {instructionError}
            </Alert>
          )}
          {instructionPath && (
            <Alert severity="success">
              Resumo salvo em: {instructionPath}
            </Alert>
          )}

          <Paper sx={{ p: 2, mt: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Perguntas sobre esta rota
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Faça perguntas em linguagem natural sobre rotas, paradas ou eficiência.
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start', flexWrap: 'wrap' }}>
              <TextField
                fullWidth
                size="small"
                label="Pergunta"
                placeholder="Ex: Qual veículo tem mais paradas? Qual a distância total?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
                sx={{ flex: 1, minWidth: 200 }}
              />
              <Button variant="contained" onClick={handleAsk} disabled={askLoading}>
                {askLoading ? 'Pensando...' : 'Perguntar'}
              </Button>
            </Box>
            {askError && (
              <Alert severity="error" sx={{ mt: 2 }}>{askError}</Alert>
            )}
            {answer && (
              <Box sx={{ mt: 2, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>Resposta</Typography>
                <Typography component="div" sx={{ whiteSpace: 'pre-wrap' }}>{answer}</Typography>
              </Box>
            )}
          </Paper>

          {routes?.artifacts?.vehicle_reports && (
            <Box sx={{ mt: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>Relatório por veículo</Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {routes.artifacts.vehicle_reports.map((r, i) => (
                  <Box
                    key={i}
                    sx={{
                      p: 2,
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                    }}
                  >
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Veículo {r.vehicle_id + 1}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Carga: {r.load_kg} kg
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Quilometragem: {r.distance_km} km
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Paradas:
                    </Typography>
                    <Box component="ul" sx={{ m: 0, pl: 2 }}>
                      {r.stops.map((s, j) => (
                        <li key={j}>
                          <Typography variant="body2" component="span">
                            {s.endereco || `Ponto ${s.id}`}
                          </Typography>
                        </li>
                      ))}
                    </Box>
                  </Box>
                ))}
              </Box>
            </Box>
          )}
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Mapa da rota</Typography>
            <MapPreview mapUrl={mapUrl} />
          </Box>
        </>
      )}
    </Box>
  )
}
