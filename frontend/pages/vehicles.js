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
      <Typography variant="h5" gutterBottom>
        Veículos
      </Typography>
      <Button variant="contained" onClick={() => setOpen(true)} sx={{ mb: 2 }}>
        Cadastrar veículo
      </Button>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Nome</TableCell>
            <TableCell>Capacidade (kg)</TableCell>
            <TableCell>Autonomia (km)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {vehicles.map((v) => (
            <TableRow key={v.id}>
              <TableCell>{v.id}</TableCell>
              <TableCell>{v.name}</TableCell>
              <TableCell>{v.capacity_kg}</TableCell>
              <TableCell>{v.autonomy_km}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {vehicles.length === 0 && (
        <Typography color="text.secondary" sx={{ mt: 2 }}>
          Nenhum veículo cadastrado.
        </Typography>
      )}

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Cadastrar veículo</DialogTitle>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField fullWidth label="Nome" value={name} onChange={(e) => setName(e.target.value)} sx={{ mt: 1, mb: 1 }} />
          <TextField fullWidth type="number" label="Capacidade (kg)" value={capacityKg} onChange={(e) => setCapacityKg(Number(e.target.value))} sx={{ mb: 1 }} />
          <TextField fullWidth type="number" label="Autonomia (km)" value={autonomyKm} onChange={(e) => setAutonomyKm(Number(e.target.value))} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={loading || !name}>
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
