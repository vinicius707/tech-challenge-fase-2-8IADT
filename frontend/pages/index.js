import * as React from 'react'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import Paper from '@mui/material/Paper'
import Link from 'next/link'
import RouteIcon from '@mui/icons-material/Route'
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar'
import LocationOnIcon from '@mui/icons-material/LocationOn'

export default function Home() {
  const stats = [
    { title: 'Rotas Otimizadas', value: '24', icon: <RouteIcon fontSize="large" color="primary" />, desc: 'No último mês' },
    { title: 'Veículos Ativos', value: '5', icon: <DirectionsCarIcon fontSize="large" color="primary" />, desc: 'Prontos para operação' },
    { title: 'Endereços Cadastrados', value: '112', icon: <LocationOnIcon fontSize="large" color="primary" />, desc: 'Hospitais e postos' },
  ]

  return (
    <Box>
      <Box sx={{ mb: 6, bgcolor: 'primary.main', color: 'primary.contrastText', p: { xs: 3, md: 5 }, borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 700 }}>
            Bem-vindo ao Sistema de Distribuição
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, fontWeight: 400, opacity: 0.9 }}>
            Solução inteligente para roteamento de medicamentos e insumos médicos com integração AG e LLM.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Link href="/create" passHref legacyBehavior>
              <Button variant="contained" size="large" sx={{ bgcolor: 'white', color: 'primary.main', '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' } }}>
                Nova Rota
              </Button>
            </Link>
            <Link href="/jobs" passHref legacyBehavior>
              <Button variant="outlined" size="large" sx={{ color: 'white', borderColor: 'rgba(255,255,255,0.5)', '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' } }}>
                Ver Histórico
              </Button>
            </Link>
          </Box>
        </Box>
        <Box sx={{ position: 'absolute', right: -50, top: -50, opacity: 0.1, transform: 'scale(3)' }}>
          <RouteIcon />
        </Box>
      </Box>

      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
        Visão Geral
      </Typography>

      <Grid container spacing={3}>
        {stats.map((stat, i) => (
          <Grid item xs={12} sm={4} key={i}>
            <Paper sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 3, height: '100%' }}>
              <Box sx={{ p: 2, borderRadius: 2, bgcolor: 'primary.50' }}>
                {stat.icon}
              </Box>
              <Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {stat.value}
                </Typography>
                <Typography variant="subtitle1" color="text.secondary">
                  {stat.title}
                </Typography>
                <Typography variant="body2" color="text.disabled">
                  {stat.desc}
                </Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}
