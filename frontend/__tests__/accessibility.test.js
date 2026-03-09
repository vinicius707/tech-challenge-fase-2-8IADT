import * as React from 'react'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import Layout from '../components/Layout'
import JobCard from '../components/JobCard'

expect.extend(toHaveNoViolations)

describe('Accessibility', () => {
  it('Layout has no obvious violations', async () => {
    const { container } = render(<Layout><div>Content</div></Layout>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('JobCard has no obvious violations', async () => {
    const { container } = render(<JobCard job={{ job_id: 'test-123', status: 'finished' }} />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
