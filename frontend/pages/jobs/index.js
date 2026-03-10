import * as React from 'react'
import useSWR from 'swr'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import Alert from '@mui/material/Alert'
import { getJobs } from '../../lib/api'
import JobCard from '../../components/JobCard'

const fetcher = () => getJobs()

export default function JobsList() {
  const { data, error, mutate } = useSWR('jobs', fetcher, {
    refreshInterval: 3000,
  })

  if (error) {
    return (
      <Alert severity="error">
        Erro ao carregar jobs. Verifique se a API está rodando em {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}.
      </Alert>
    )
  }

  if (!data) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  const jobs = Object.entries(data.jobs || {}).map(([id, j]) => ({
    job_id: id,
    ...j,
  }))

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Planejamentos de rotas
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
        {jobs.length === 0 ? (
          <Typography color="text.secondary">Nenhum planejamento ainda.</Typography>
        ) : (
          jobs.map((job) => <JobCard key={job.job_id} job={job} />)
        )}
      </Box>
    </Box>
  )
}
