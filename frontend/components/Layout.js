import * as React from 'react'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Container from '@mui/material/Container'
import Link from 'next/link'
import { Box } from '@mui/material'

const navLinks = [
  { href: '/', label: 'Início' },
  { href: '/create', label: 'Criar Job' },
  { href: '/jobs', label: 'Jobs' },
]

export default function Layout({ children }) {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Tech Challenge — Rotas
          </Typography>
          <Box component="nav" sx={{ display: 'flex', gap: { xs: 1, sm: 2 }, flexWrap: 'wrap' }}>
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                style={{ color: 'white', textDecoration: 'none' }}
              >
                {link.label}
              </Link>
            ))}
          </Box>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flex: 1, py: 3 }}>
        {children}
      </Container>
    </Box>
  )
}
