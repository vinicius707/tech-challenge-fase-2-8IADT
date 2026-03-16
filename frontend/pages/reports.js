import * as React from 'react'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Paper from '@mui/material/Paper'
import Alert from '@mui/material/Alert'
import CircularProgress from '@mui/material/CircularProgress'
import { getWeeklyReport } from '../lib/api'

export default function Reports() {
  const [fromDate, setFromDate] = React.useState('')
  const [toDate, setToDate] = React.useState('')
  const [data, setData] = React.useState(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  const handleSubmit = async () => {
    setError(null)
    setData(null)
    setLoading(true)
    try {
      const res = await getWeeklyReport(fromDate || undefined, toDate || undefined)
      setData(res)
    } catch (e) {
      setError(e.message || 'Erro ao gerar relatório')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Relatórios logísticos
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Selecione o período (formato YYYY-MM-DD). Deixe em branco para os últimos 7 dias.
      </Typography>
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 3 }}>
        <TextField label="De" type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} InputLabelProps={{ shrink: true }} />
        <TextField label="Até" type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} InputLabelProps={{ shrink: true }} />
        <Button variant="contained" onClick={handleSubmit} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Gerar relatório'}
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {data && (
        <Box>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>Métricas</Typography>
            <pre style={{ fontSize: 14, overflow: 'auto' }}>{JSON.stringify(data.metrics, null, 2)}</pre>
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Resumo (LLM)</Typography>
            <Typography component="div" sx={{ whiteSpace: 'pre-wrap' }}>{data.summary}</Typography>
          </Paper>
        </Box>
      )}
    </Box>
  )
}
