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
import { getLocations, postLocation } from '../lib/api'

const fetcher = () => getLocations().then((r) => r.locations || [])

export default function Locations() {
  const { data: locations = [], mutate } = useSWR('locations', fetcher)
  const [open, setOpen] = React.useState(false)
  const [address, setAddress] = React.useState('')
  const [lat, setLat] = React.useState(-23.55)
  const [lon, setLon] = React.useState(-46.63)
  const [priority, setPriority] = React.useState('ALTA')
  const [notes, setNotes] = React.useState('')
  const [error, setError] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  const handleSubmit = async () => {
    setError(null)
    setLoading(true)
    try {
      await postLocation({ address, lat, lon, priority, notes })
      mutate()
      setOpen(false)
      setAddress('')
      setLat(-23.55)
      setLon(-46.63)
      setPriority('ALTA')
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
        Endereços
      </Typography>
      <Button variant="contained" onClick={() => setOpen(true)} sx={{ mb: 2 }}>
        Cadastrar local
      </Button>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Endereço</TableCell>
            <TableCell>Lat/Lon</TableCell>
            <TableCell>Prioridade</TableCell>
            <TableCell>Notas</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {locations.map((loc) => (
            <TableRow key={loc.id}>
              <TableCell>{loc.id}</TableCell>
              <TableCell>{loc.address}</TableCell>
              <TableCell>{loc.lat?.toFixed(4)}, {loc.lon?.toFixed(4)}</TableCell>
              <TableCell>{loc.priority}</TableCell>
              <TableCell>{loc.notes}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {locations.length === 0 && (
        <Typography color="text.secondary" sx={{ mt: 2 }}>
          Nenhum local cadastrado.
        </Typography>
      )}

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Cadastrar local</DialogTitle>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField fullWidth label="Endereço" value={address} onChange={(e) => setAddress(e.target.value)} sx={{ mt: 1, mb: 1 }} />
          <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
            <TextField type="number" label="Lat" value={lat} onChange={(e) => setLat(Number(e.target.value))} />
            <TextField type="number" label="Lon" value={lon} onChange={(e) => setLon(Number(e.target.value))} />
          </Box>
          <FormControl fullWidth sx={{ mt: 1 }}>
            <InputLabel>Prioridade</InputLabel>
            <Select value={priority} label="Prioridade" onChange={(e) => setPriority(e.target.value)}>
              <MenuItem value="ALTA">ALTA</MenuItem>
              <MenuItem value="MÉDIA">MÉDIA</MenuItem>
              <MenuItem value="BAIXA">BAIXA</MenuItem>
            </Select>
          </FormControl>
          <TextField fullWidth label="Notas" value={notes} onChange={(e) => setNotes(e.target.value)} sx={{ mt: 1 }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !address}>
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
