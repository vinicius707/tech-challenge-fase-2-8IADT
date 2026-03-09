import * as React from 'react'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Link from 'next/link'

export default function Home() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Otimização de Rotas Médicas
      </Typography>
      <Typography variant="body1" paragraph>
        Crie jobs de otimização, acompanhe o progresso e visualize os artefatos gerados.
      </Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
        <Link href="/create" passHref legacyBehavior>
          <Button variant="contained">Criar novo job</Button>
        </Link>
        <Link href="/jobs" passHref legacyBehavior>
          <Button variant="outlined">Ver jobs</Button>
        </Link>
      </Box>
    </Box>
  )
}
