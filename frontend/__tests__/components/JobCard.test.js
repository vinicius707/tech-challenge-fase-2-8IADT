import * as React from 'react'
import { render, screen } from '@testing-library/react'
import JobCard from '../../components/JobCard'

describe('JobCard', () => {
  it('renders correctly', () => {
    const job = { job_id: 'xyz-999', status: 'finished' }
    render(<JobCard job={job} />)
    expect(screen.getByText(/ID: XYZ-999/)).toBeInTheDocument()
    expect(screen.getByText('Concluído')).toBeInTheDocument()
  })

  it('renders link to details', () => {
    const job = { job_id: 'xyz-999', status: 'running' }
    render(<JobCard job={job} />)
    expect(screen.getByRole('link', { name: /Ver Detalhes do Plano/ })).toHaveAttribute('href', '/jobs/xyz-999')
  })
})
