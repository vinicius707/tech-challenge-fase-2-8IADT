import * as React from 'react'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Link from 'next/link'

export default function Home() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Planejamento de Rotas de Distribuição
      </Typography>
      <Typography variant="body1" paragraph>
        Planeje rotas de distribuição, acompanhe o progresso e visualize os resultados gerados.
      </Typography>
      <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
        <Link href="/create" passHref legacyBehavior>
          <Button variant="contained">Planejar rota</Button>
        </Link>
        <Link href="/jobs" passHref legacyBehavior>
          <Button variant="outlined">Ver planejamentos</Button>
        </Link>
      </Box>
    </Box>
  )
}
