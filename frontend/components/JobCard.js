import * as React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from '@mui/material/CardActions'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import Link from 'next/link'
import Box from '@mui/material/Box'
import AssessmentIcon from '@mui/icons-material/Assessment'
import CircularProgress from '@mui/material/CircularProgress'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import PendingIcon from '@mui/icons-material/Pending'

const statusColors = {
  queued: 'default',
  running: 'info',
  finished: 'success',
  failed: 'error',
}

const statusLabels = {
  queued: 'Na fila',
  running: 'Em execução',
  finished: 'Concluído',
  failed: 'Falhou',
}

const statusIcons = {
  queued: <PendingIcon fontSize="small" />,
  running: <CircularProgress size={16} color="inherit" />,
  finished: <CheckCircleIcon fontSize="small" />,
  failed: <ErrorIcon fontSize="small" />,
}

export default function JobCard({ job }) {
  const { job_id, status } = job
  const color = statusColors[status] || 'default'

  return (
    <Card 
      sx={{ 
        minWidth: 260, 
        width: { xs: '100%', sm: 300 },
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        }
      }}
    >
      <CardContent sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ bgcolor: 'primary.50', p: 1, borderRadius: 2 }}>
            <AssessmentIcon color="primary" />
          </Box>
          <Chip 
            icon={statusIcons[status]} 
            label={statusLabels[status] || status} 
            color={color} 
            size="small" 
            variant="outlined" 
            sx={{ fontWeight: 600, bgcolor: `${color}.50` }} 
          />
        </Box>
        <Typography variant="overline" color="text.secondary" sx={{ fontWeight: 600, letterSpacing: 1 }}>
          ID: {job_id?.slice(0, 8).toUpperCase()}
        </Typography>
        <Typography variant="h6" component="div" sx={{ mt: 0.5, fontWeight: 700, lineHeight: 1.2 }}>
          Rotas de Distribuição
        </Typography>
      </CardContent>
      <CardActions sx={{ px: 2, pb: 2, pt: 1 }}>
        <Link href={`/jobs/${job_id}`} passHref legacyBehavior>
          <Button variant="contained" disableElevation fullWidth size="medium">
            Ver Detalhes do Plano
          </Button>
        </Link>
      </CardActions>
    </Card>
  )
}
