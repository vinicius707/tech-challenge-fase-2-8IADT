import * as React from 'react'
import useSWR from 'swr'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
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
import { getVehicles, postVehicle } from '../lib/api'

const fetcher = () => getVehicles().then((r) => r.vehicles || [])

export default function Vehicles() {
  const { data: vehicles = [], mutate } = useSWR('vehicles', fetcher)
  const [open, setOpen] = React.useState(false)
  const [name, setName] = React.useState('')
  const [capacityKg, setCapacityKg] = React.useState(200)
  const [autonomyKm, setAutonomyKm] = React.useState(300)
  const [error, setError] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  const handleSubmit = async () => {
    setError(null)
    setLoading(true)
    try {
      await postVehicle({ name, capacity_kg: capacityKg, autonomy_km: autonomyKm })
      mutate()
      setOpen(false)
      setName('')
      setCapacityKg(200)
      setAutonomyKm(300)
    } catch (e) {
      setError(e.message || 'Erro ao salvar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Veículos Cadastrados
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)}>
          Novo Veículo
        </Button>
      </Box>

      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead sx={{ bgcolor: 'secondary.main' }}>
            <TableRow>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>ID</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Nome</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Capacidade (kg)</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Autonomia (km)</TableCell>
              <TableCell sx={{ color: 'secondary.contrastText', fontWeight: 600 }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {vehicles.map((v) => (
              <TableRow key={v.id} hover>
                <TableCell>{v.id}</TableCell>
                <TableCell sx={{ fontWeight: 500 }}>{v.name}</TableCell>
                <TableCell>{v.capacity_kg} kg</TableCell>
                <TableCell>{v.autonomy_km} km</TableCell>
                <TableCell>
                  <Chip label="Ativo" color="success" size="small" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {vehicles.length === 0 && (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="text.secondary">Nenhum veículo cadastrado.</Typography>
          </Box>
        )}
      </Paper>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 600 }}>Cadastrar Veículo</DialogTitle>
        <DialogContent dividers>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField fullWidth label="Modelo / Placa" value={name} onChange={(e) => setName(e.target.value)} sx={{ mt: 1, mb: 3 }} />
          <TextField fullWidth type="number" label="Capacidade Máxima (kg)" value={capacityKg} onChange={(e) => setCapacityKg(Number(e.target.value))} sx={{ mb: 3 }} />
          <TextField fullWidth type="number" label="Autonomia Total (km)" value={autonomyKm} onChange={(e) => setAutonomyKm(Number(e.target.value))} />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !name}>
            Salvar Veículo
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
