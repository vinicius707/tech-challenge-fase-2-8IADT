import * as React from 'react'
import { render, screen } from '@testing-library/react'
import MapPreview from '../../components/MapPreview'

describe('MapPreview', () => {
  it('renders fallback when no mapUrl', () => {
    render(<MapPreview mapUrl={null} />)
    expect(screen.getByText(/Mapa não disponível/)).toBeInTheDocument()
  })

  it('renders iframe when mapUrl provided', () => {
    render(<MapPreview mapUrl="test.html" />)
    expect(screen.getByTestId('map-iframe')).toHaveAttribute('src', 'test.html')
  })
})
