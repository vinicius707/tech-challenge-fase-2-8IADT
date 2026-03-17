import * as React from 'react'
import useSWR from 'swr'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import InputLabel from '@mui/material/InputLabel'
import FormControl from '@mui/material/FormControl'
import Dialog from '@mui/material/Dialog'
import DialogTitle from '@mui/material/DialogTitle'
import DialogContent from '@mui/material/DialogContent'
import DialogActions from '@mui/material/DialogActions'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Alert from '@mui/material/Alert'
import Paper from '@mui/material/Paper'
import AddIcon from '@mui/icons-material/Add'
import Chip from '@mui/material/Chip'
import { getDeliveries, postDelivery, getLocations } from '../lib/api'

const deliveriesFetcher = () => getDeliveries().then((r) => r.deliveries || [])
const locationsFetcher = () => getLocations().then((r) => r.locations || [])

export default function Deliveries() {
  const { data: deliveries = [], mutate } = useSWR('deliveries', deliveriesFetcher)
  const { data: locations = [] } = useSWR('locations', locationsFetcher)
  const [open, setOpen] = React.useState(false)
  const [locationId, setLocationId] = React.useState('')
  const [priority, setPriority] = React.useState('CRÍTICA')
  const [volumeKg, setVolumeKg] = React.useState(0)
  const [notes, setNotes] = React.useState('')
  const [error, setError] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  const locById = React.useMemo(() => Object.fromEntries(locations.map((l) => [l.id, l])), [locations])

  const handleSubmit = async () => {
    setError(null)
    setLoading(true)
    try {
      await postDelivery({ location_id: Number(locationId), priority, volume_kg: volumeKg, notes })
      mutate()
      setOpen(false)
      setLocationId('')
      setPriority('CRÍTICA')
      setVolumeKg(0)
      setNotes('')
    } catch (e) {
      setError(e.message || 'Erro ao salvar')
    } finally {
      setLoading(false)
    }
  }

  const getPriorityColor = (p) => {
    switch(p) {
      case 'CRÍTICA': return 'error'
      case 'ALTA': return 'warning'
      case 'MÉDIA': return 'info'
      case 'BAIXA': return 'default'
      default: return 'default'
    }
  }

  const getStatusColor = (s) => {
    if (s === 'pendente') return 'warning'
    if (s === 'entregue') return 'success'
    return 'default'
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Encomendas e Insumos
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)} disabled={locations.length === 0}>
          Registrar Entrega
        </Button>
      </Box>

      {locations.length === 0 && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          Nenhum local cadastrado. Cadastre Hospitais/Postos antes de registrar entregas.
        </Alert>
      )}

      <Paper sx={{ width: '100%', overflowX: 'auto' }}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead sx={{ bgcolor: 'secondary.main' }}>
            <TableRow>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>ID</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Local de Destino</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Prioridade</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Peso/Volume</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deliveries.map((d) => (
              <TableRow key={d.id} hover>
                <TableCell>{d.id}</TableCell>
                <TableCell sx={{ fontWeight: 500 }}>{locById[d.location_id]?.address || `Local #${d.location_id}`}</TableCell>
                <TableCell>
                  <Chip 
                    label={d.priority} 
                    color={getPriorityColor(d.priority)} 
                    size="small" 
                    variant="outlined"
                    sx={{ fontWeight: 600 }}
                  />
                </TableCell>
                <TableCell>{d.volume_kg} kg</TableCell>
                <TableCell>
                  <Chip 
                    label={d.status?.toUpperCase() || 'PENDENTE'} 
                    color={getStatusColor(d.status || 'pendente')} 
                    size="small" 
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {deliveries.length === 0 && locations.length > 0 && (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">Nenhuma entrega agendada no momento.</Typography>
          </Box>
        )}
      </Paper>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 600 }}>Registrar Nova Entrega</DialogTitle>
        <DialogContent dividers>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <FormControl fullWidth sx={{ mt: 1, mb: 3 }}>
            <InputLabel>Hospital/Posto de Destino</InputLabel>
            <Select value={locationId} label="Hospital/Posto de Destino" onChange={(e) => setLocationId(e.target.value)}>
              {locations.map((l) => (
                <MenuItem key={l.id} value={l.id}>{l.address} (ID: {l.id})</MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Prioridade da Encomenda</InputLabel>
            <Select value={priority} label="Prioridade da Encomenda" onChange={(e) => setPriority(e.target.value)}>
              <MenuItem value="CRÍTICA">Crítica (Medicamentos urgentes)</MenuItem>
              <MenuItem value="ALTA">Alta (Urgência)</MenuItem>
              <MenuItem value="MÉDIA">Média (Rotina regular)</MenuItem>
              <MenuItem value="BAIXA">Baixa (Insumos gerais)</MenuItem>
            </Select>
          </FormControl>

          <TextField fullWidth type="number" label="Peso Total / Volume Estimado (kg)" value={volumeKg} onChange={(e) => setVolumeKg(Number(e.target.value))} sx={{ mb: 3 }} />
          <TextField fullWidth label="Instruções Específicas / Notas" value={notes} onChange={(e) => setNotes(e.target.value)} multiline rows={2} />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !locationId}>
            Salvar Entrega
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
