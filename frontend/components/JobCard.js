import * as React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActions from '@mui/material/CardActions'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import Link from 'next/link'

const statusColors = {
  queued: 'default',
  running: 'info',
  finished: 'success',
  failed: 'error',
}

export default function JobCard({ job }) {
  const { job_id, status } = job
  const color = statusColors[status] || 'default'

  return (
    <Card variant="outlined" sx={{ minWidth: 260, width: { xs: '100%', sm: 280 } }}>
      <CardContent>
        <Typography variant="overline" color="text.secondary">
          {job_id?.slice(0, 8)}…
        </Typography>
        <Typography variant="h6" component="div" sx={{ mt: 0.5 }}>
          Job {job_id?.slice(0, 8)}
        </Typography>
        <Chip label={status} color={color} size="small" sx={{ mt: 1 }} />
      </CardContent>
      <CardActions>
        <Link href={`/jobs/${job_id}`} passHref legacyBehavior>
          <Button size="small">Ver detalhes</Button>
        </Link>
      </CardActions>
    </Card>
  )
}
