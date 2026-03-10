import * as React from 'react'
import { useRouter } from 'next/router'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Alert from '@mui/material/Alert'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import { postOptimize } from '../lib/api'
import useSWR from 'swr'
import { getDeliveries, getVehicles } from '../lib/api'

const deliveriesFetcher = () => getDeliveries().then((r) => r.deliveries || [])
const vehiclesFetcher = () => getVehicles().then((r) => r.vehicles || [])

export default function Create() {
  const router = useRouter()
  const { data: deliveries = [] } = useSWR('deliveries', deliveriesFetcher)
  const { data: vehicles = [] } = useSWR('vehicles', vehiclesFetcher)

  const [useDynamic, setUseDynamic] = React.useState(false)
  const [instance, setInstance] = React.useState('data/instances/hospital_points.csv')
  const [numVehicles, setNumVehicles] = React.useState(3)
  const [deliveryIds, setDeliveryIds] = React.useState([])
  const [vehicleIds, setVehicleIds] = React.useState([])
  const [population, setPopulation] = React.useState(50)
  const [generations, setGenerations] = React.useState(100)
  const [mutationRate, setMutationRate] = React.useState(0.05)
  const [elitism, setElitism] = React.useState(1)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState(null)
  const [deliveriesOpen, setDeliveriesOpen] = React.useState(false)
  const [vehiclesOpen, setVehiclesOpen] = React.useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const params = {
        population,
        generations,
        mutation_rate: mutationRate,
        elitism,
      }
      if (useDynamic && deliveryIds.length > 0 && vehicleIds.length > 0) {
        params.delivery_ids = deliveryIds
        params.vehicle_ids = vehicleIds
      } else if (useDynamic) {
        throw new Error('Selecione ao menos uma encomenda e um veículo ao usar dados cadastrados.')
      } else {
        params.instance = instance
        params.num_vehicles = numVehicles
      }
      const res = await postOptimize(params)
      router.push(`/jobs/${res.job_id}`)
    } catch (err) {
      const detail = err.body?.detail
      const detailStr = Array.isArray(detail) ? detail.join(', ') : detail
      const msg = err.status === 404 || err.message?.includes('fetch')
        ? 'Não foi possível conectar à API. Verifique se o backend está rodando (porta 8000).'
        : (detailStr || err.message || 'Erro ao planejar rota')
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 560 }}>
      <Typography variant="h5" gutterBottom>
        Planejar rota de distribuição
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      <FormControlLabel
        control={<Checkbox checked={useDynamic} onChange={(e) => setUseDynamic(e.target.checked)} />}
        label="Usar dados cadastrados (encomendas e veículos)"
        sx={{ mb: 2, display: 'block' }}
      />

      {useDynamic ? (
        <Box sx={{ mb: 2 }}>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Encomendas</InputLabel>
            <Select
              multiple
              open={deliveriesOpen}
              onOpen={() => setDeliveriesOpen(true)}
              onClose={() => setDeliveriesOpen(false)}
              value={deliveryIds}
              label="Encomendas"
              onChange={(e) => {
                setDeliveryIds(e.target.value)
                setDeliveriesOpen(false)
              }}
              renderValue={(sel) => sel.join(', ')}
            >
              {deliveries.map((d) => (
                <MenuItem key={d.id} value={d.id}>#{d.id} – {d.priority}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Veículos</InputLabel>
            <Select
              multiple
              open={vehiclesOpen}
              onOpen={() => setVehiclesOpen(true)}
              onClose={() => setVehiclesOpen(false)}
              value={vehicleIds}
              label="Veículos"
              onChange={(e) => {
                setVehicleIds(e.target.value)
                setVehiclesOpen(false)
              }}
              renderValue={(sel) => sel.join(', ')}
            >
              {vehicles.filter((v) => v.active !== false).map((v) => (
                <MenuItem key={v.id} value={v.id}>{v.name} ({v.capacity_kg}kg, {v.autonomy_km}km)</MenuItem>
              ))}
            </Select>
          </FormControl>
          {(deliveries.length === 0 || vehicles.length === 0) && (
            <Alert severity="info" sx={{ mt: 1 }}>
              Cadastre encomendas e veículos nas páginas Encomendas e Veículos.
            </Alert>
          )}
        </Box>
      ) : (
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            label="Arquivo de pontos (CSV)"
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
          />
        </Box>
      )}

      <Accordion sx={{ mb: 2 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Configurações avançadas</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              type="number"
              label="População"
              value={population}
              onChange={(e) => setPopulation(Number(e.target.value))}
              inputProps={{ min: 10 }}
            />
            <TextField
              fullWidth
              type="number"
              label="Gerações"
              value={generations}
              onChange={(e) => setGenerations(Number(e.target.value))}
              inputProps={{ min: 1 }}
            />
            <TextField
              fullWidth
              type="number"
              label="Taxa de mutação"
              value={mutationRate}
              onChange={(e) => setMutationRate(Number(e.target.value))}
              inputProps={{ min: 0, max: 1, step: 0.01 }}
            />
            <TextField
              fullWidth
              type="number"
              label="Elitismo"
              value={elitism}
              onChange={(e) => setElitism(Number(e.target.value))}
              inputProps={{ min: 0 }}
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      <Button type="submit" variant="contained" disabled={loading}>
        {loading ? 'Planejando…' : 'Planejar rota'}
      </Button>
    </Box>
  )
}
