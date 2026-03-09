import * as React from 'react'
import { render, screen } from '@testing-library/react'
import MapPreview from '../../components/MapPreview'

describe('MapPreview', () => {
  it('renders fallback when no mapUrl', () => {
    render(<MapPreview mapUrl={null} />)
    expect(screen.getByText(/Mapa de rotas não disponível/)).toBeInTheDocument()
  })

  it('renders iframe when mapUrl provided', () => {
    render(<MapPreview mapUrl="/test/route_map.html" />)
    const iframe = document.querySelector('iframe[title="Mapa de rotas"]')
    expect(iframe).toBeInTheDocument()
    expect(iframe).toHaveAttribute('src', '/test/route_map.html')
  })
})
