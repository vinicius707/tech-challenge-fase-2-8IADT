import * as React from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Alert from '@mui/material/Alert'

/**
 * Mostra preview do mapa de rotas via iframe (ou link fallback).
 * @param {string} mapUrl - URL do route_map.html ou null se não disponível
 */
export default function MapPreview({ mapUrl }) {
  if (!mapUrl) {
    return (
      <Alert severity="info">
        Mapa não disponível. Planeje a rota e aguarde a conclusão.
      </Alert>
    )
  }

  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <iframe
        src={mapUrl}
        title="Mapa de rotas"
        data-testid="map-iframe"
        style={{ width: '100%', height: '100%', border: '1px solid #ccc' }}
      />
    </Box>
  )
}
