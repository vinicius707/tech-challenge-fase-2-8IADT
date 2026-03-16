import React from 'react'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import JobCard from '../components/JobCard'

describe('JobCard', () => {
  it('renders correctly with queued status', () => {
    const job = { job_id: 'test-123', status: 'queued' }
    render(<JobCard job={job} />)
    
    expect(screen.getByText(/ID: TEST-123/i)).toBeInTheDocument()
    expect(screen.getByText('Na fila')).toBeInTheDocument()
    expect(screen.getByText('Rotas de Distribuição')).toBeInTheDocument()
  })

  it('renders correctly with finished status', () => {
    const job = { job_id: 'test-xyz', status: 'finished' }
    render(<JobCard job={job} />)
    
    expect(screen.getByText(/ID: TEST-XYZ/i)).toBeInTheDocument()
    expect(screen.getByText('Concluído')).toBeInTheDocument()
  })
})
