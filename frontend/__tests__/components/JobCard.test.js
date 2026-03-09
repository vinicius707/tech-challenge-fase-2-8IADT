import * as React from 'react'
import { render, screen } from '@testing-library/react'
import JobCard from '../../components/JobCard'

describe('JobCard', () => {
  it('renders job summary', () => {
    const job = { job_id: 'abc12345-1234-5678', status: 'finished' }
    render(<JobCard job={job} />)
    expect(screen.getByText(/Job abc12345/)).toBeInTheDocument()
    expect(screen.getByText('finished')).toBeInTheDocument()
  })

  it('renders link to details', () => {
    const job = { job_id: 'xyz-999', status: 'running' }
    render(<JobCard job={job} />)
    expect(screen.getByRole('link', { name: /Ver detalhes/ })).toHaveAttribute('href', '/jobs/xyz-999')
  })
})
