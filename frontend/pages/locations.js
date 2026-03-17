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

  const getPriorityColor = (p) => {
    switch(p) {
      case 'ALTA': return 'error'
      case 'MÉDIA': return 'warning'
      case 'BAIXA': return 'info'
      default: return 'default'
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Endereços / Hospitais
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)}>
          Novo Local
        </Button>
      </Box>

      <Paper sx={{ width: '100%', overflowX: 'auto' }}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead sx={{ bgcolor: 'secondary.main' }}>
            <TableRow>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>ID</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Endereço</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Lat/Lon</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Prioridade Padrão</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Notas</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {locations.map((loc) => (
              <TableRow key={loc.id} hover>
                <TableCell>{loc.id}</TableCell>
                <TableCell sx={{ fontWeight: 500 }}>{loc.address}</TableCell>
                <TableCell sx={{ color: 'text.secondary' }}>{loc.lat?.toFixed(4)}, {loc.lon?.toFixed(4)}</TableCell>
                <TableCell>
                  <Chip 
                    label={loc.priority} 
                    color={getPriorityColor(loc.priority)} 
                    size="small" 
                    variant="outlined"
                    sx={{ fontWeight: 600 }}
                  />
                </TableCell>
                <TableCell>{loc.notes}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {locations.length === 0 && (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">Nenhum local cadastrado.</Typography>
          </Box>
        )}
      </Paper>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 600 }}>Cadastrar Local</DialogTitle>
        <DialogContent dividers>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField fullWidth label="Endereço Completo" value={address} onChange={(e) => setAddress(e.target.value)} sx={{ mt: 1, mb: 3 }} />
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            <TextField type="number" label="Latitude" value={lat} onChange={(e) => setLat(Number(e.target.value))} fullWidth />
            <TextField type="number" label="Longitude" value={lon} onChange={(e) => setLon(Number(e.target.value))} fullWidth />
          </Box>
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Prioridade Padrão</InputLabel>
            <Select value={priority} label="Prioridade Padrão" onChange={(e) => setPriority(e.target.value)}>
              <MenuItem value="ALTA">Alta (Urgência)</MenuItem>
              <MenuItem value="MÉDIA">Média (Rotina)</MenuItem>
              <MenuItem value="BAIXA">Baixa (Insumos gerais)</MenuItem>
            </Select>
          </FormControl>
          <TextField fullWidth label="Observações de Acesso" value={notes} onChange={(e) => setNotes(e.target.value)} multiline rows={2} />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !address}>
            Salvar Local
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
