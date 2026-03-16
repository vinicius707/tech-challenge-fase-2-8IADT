import React from 'react'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import Layout from '../components/Layout'

// Mock next/router
jest.mock('next/router', () => ({
  useRouter: () => ({
    pathname: '/',
    push: jest.fn(),
  }),
}))

describe('Layout', () => {
  it('renders the sidebar navigation and children', () => {
    render(
      <Layout>
        <div data-testid="child-content">Conteúdo da Criança</div>
      </Layout>
    )
    
    // Check Top Bar Title
    expect(screen.getByText('Planejamento de Rotas')).toBeInTheDocument()
    // Check Sidebar Brand
    expect(screen.getByText('Distribuição')).toBeInTheDocument()
    
    // Check standard links
    expect(screen.getByText('Planejar Rota')).toBeInTheDocument()
    expect(screen.getByText('Veículos')).toBeInTheDocument()
    expect(screen.getByText('Encomendas')).toBeInTheDocument()

    // Check children rendering
    expect(screen.getByTestId('child-content')).toBeInTheDocument()
  })
})
