import * as React from 'react'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import Alert from '@mui/material/Alert'
import Chip from '@mui/material/Chip'
import { getJob, getRoutes, postInstructions } from '../../lib/api'
import MapPreview from '../../components/MapPreview'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function JobDetail() {
  const router = useRouter()
  const { id } = router.query
  const [instructionPath, setInstructionPath] = React.useState(null)
  const [instructionLoading, setInstructionLoading] = React.useState(false)
  const [instructionError, setInstructionError] = React.useState(null)

  const { data: job, error: jobError } = useSWR(
    id ? `job-${id}` : null,
    () => getJob(id),
    { refreshInterval: 2000 }
  )

  const { data: routes } = useSWR(
    id ? `routes-${id}` : null,
    () => getRoutes(id),
    { refreshInterval: job?.status === 'finished' ? 0 : 2000 }
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
    return <Alert severity="error">Job não encontrado.</Alert>
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
        Job {id.slice(0, 8)}
      </Typography>
      <Chip label={job.status} color={job.status === 'finished' ? 'success' : 'default'} sx={{ mb: 2 }} />

      {job.error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {job.error}
        </Alert>
      )}

      {historyUrl && (
        <Box sx={{ mb: 2 }}>
          <Button href={historyUrl} target="_blank" rel="noopener" component="a">
            Baixar history.csv
          </Button>
        </Box>
      )}

      {job.status === 'finished' && (
        <>
          <Box sx={{ mb: 2 }}>
            <Button variant="contained" onClick={handleExport} sx={{ mr: 2 }}>
              Abrir mapa (route_map.html)
            </Button>
            <Button
              variant="outlined"
              onClick={handleGenerateInstructions}
              disabled={instructionLoading}
            >
              {instructionLoading ? 'Gerando…' : 'Gerar instruções'}
            </Button>
          </Box>
          {instructionError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {instructionError}
            </Alert>
          )}
          {instructionPath && (
            <Alert severity="success">
              Instruções salvas em: {instructionPath}
            </Alert>
          )}
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Preview do mapa</Typography>
            <MapPreview mapUrl={mapUrl} />
          </Box>
        </>
      )}
    </Box>
  )
}
