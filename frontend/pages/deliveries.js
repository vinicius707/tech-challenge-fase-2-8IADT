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

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Encomendas
      </Typography>
      <Button variant="contained" onClick={() => setOpen(true)} disabled={locations.length === 0} sx={{ mb: 2 }}>
        Registrar entrega
      </Button>
      {locations.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>Cadastre locais antes de registrar entregas.</Alert>
      )}
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Local</TableCell>
            <TableCell>Prioridade</TableCell>
            <TableCell>Volume (kg)</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {deliveries.map((d) => (
            <TableRow key={d.id}>
              <TableCell>{d.id}</TableCell>
              <TableCell>{locById[d.location_id]?.address || `#${d.location_id}`}</TableCell>
              <TableCell>{d.priority}</TableCell>
              <TableCell>{d.volume_kg}</TableCell>
              <TableCell>{d.status}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {deliveries.length === 0 && locations.length > 0 && (
        <Typography color="text.secondary" sx={{ mt: 2 }}>
          Nenhuma entrega registrada.
        </Typography>
      )}

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Registrar entrega</DialogTitle>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <FormControl fullWidth sx={{ mt: 1, mb: 1 }}>
            <InputLabel>Local</InputLabel>
            <Select value={locationId} label="Local" onChange={(e) => setLocationId(e.target.value)}>
              {locations.map((l) => (
                <MenuItem key={l.id} value={l.id}>{l.address} (id {l.id})</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth sx={{ mb: 1 }}>
            <InputLabel>Prioridade</InputLabel>
            <Select value={priority} label="Prioridade" onChange={(e) => setPriority(e.target.value)}>
              <MenuItem value="CRÍTICA">CRÍTICA</MenuItem>
              <MenuItem value="ALTA">ALTA</MenuItem>
              <MenuItem value="MÉDIA">MÉDIA</MenuItem>
              <MenuItem value="BAIXA">BAIXA</MenuItem>
            </Select>
          </FormControl>
          <TextField fullWidth type="number" label="Volume (kg)" value={volumeKg} onChange={(e) => setVolumeKg(Number(e.target.value))} sx={{ mb: 1 }} />
          <TextField fullWidth label="Notas" value={notes} onChange={(e) => setNotes(e.target.value)} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !locationId}>
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
