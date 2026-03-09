import * as React from 'react'
import { useRouter } from 'next/router'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Alert from '@mui/material/Alert'
import { postOptimize } from '../lib/api'

export default function Create() {
  const router = useRouter()
  const [instance, setInstance] = React.useState('data/instances/hospital_points.csv')
  const [numVehicles, setNumVehicles] = React.useState(3)
  const [population, setPopulation] = React.useState(50)
  const [generations, setGenerations] = React.useState(100)
  const [mutationRate, setMutationRate] = React.useState(0.05)
  const [elitism, setElitism] = React.useState(1)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await postOptimize({
        instance,
        num_vehicles: numVehicles,
        population,
        generations,
        mutation_rate: mutationRate,
        elitism,
      })
      router.push(`/jobs/${res.job_id}`)
    } catch (err) {
      const detail = err.body?.detail
      const detailStr = Array.isArray(detail) ? detail.join(', ') : detail
      const msg = err.status === 404 || err.message?.includes('fetch')
        ? 'Não foi possível conectar à API. Verifique se o backend está rodando (porta 8000).'
        : (detailStr || err.message || 'Erro ao criar job')
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 480 }}>
      <Typography variant="h5" gutterBottom>
        Criar job de otimização
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      <TextField
        fullWidth
        label="Instância (CSV)"
        value={instance}
        onChange={(e) => setInstance(e.target.value)}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        type="number"
        label="Nº veículos"
        value={numVehicles}
        onChange={(e) => setNumVehicles(Number(e.target.value))}
        inputProps={{ min: 1 }}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        type="number"
        label="População"
        value={population}
        onChange={(e) => setPopulation(Number(e.target.value))}
        inputProps={{ min: 10 }}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        type="number"
        label="Gerações"
        value={generations}
        onChange={(e) => setGenerations(Number(e.target.value))}
        inputProps={{ min: 1 }}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        type="number"
        label="Taxa de mutação"
        value={mutationRate}
        onChange={(e) => setMutationRate(Number(e.target.value))}
        inputProps={{ min: 0, max: 1, step: 0.01 }}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        type="number"
        label="Elitismo"
        value={elitism}
        onChange={(e) => setElitism(Number(e.target.value))}
        inputProps={{ min: 0 }}
        sx={{ mb: 2 }}
      />
      <Button type="submit" variant="contained" disabled={loading}>
        {loading ? 'Criando…' : 'Criar job'}
      </Button>
    </Box>
  )
}
