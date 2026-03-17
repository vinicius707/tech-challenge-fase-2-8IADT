import * as React from 'react'
import { styled, useTheme } from '@mui/material/styles'
import Box from '@mui/material/Box'
import MuiDrawer from '@mui/material/Drawer'
import MuiAppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import List from '@mui/material/List'
import CssBaseline from '@mui/material/CssBaseline'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import IconButton from '@mui/material/IconButton'
import MenuIcon from '@mui/icons-material/Menu'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import { useRouter } from 'next/router'
import HomeIcon from '@mui/icons-material/Home'
import RouteIcon from '@mui/icons-material/Route'
import ViewListIcon from '@mui/icons-material/ViewList'
import LocationOnIcon from '@mui/icons-material/LocationOn'
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar'
import LocalShippingIcon from '@mui/icons-material/LocalShipping'
import AssessmentIcon from '@mui/icons-material/Assessment'

const drawerWidth = 260

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
  backgroundColor: theme.palette.secondary.main,
  color: theme.palette.secondary.contrastText,
})

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
  backgroundColor: theme.palette.secondary.main,
  color: theme.palette.secondary.contrastText,
})

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}))

const AppBarDesktop = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  backgroundColor: theme.palette.background.paper,
  color: theme.palette.text.primary,
  boxShadow: 'none',
  borderBottom: `1px solid ${theme.palette.divider}`,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}))

const DrawerDesktop = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
)

const navLinks = [
  { href: '/', label: 'Início', icon: <HomeIcon /> },
  { href: '/create', label: 'Planejar Rota', icon: <RouteIcon /> },
  { href: '/jobs', label: 'Histórico', icon: <ViewListIcon /> },
  { href: '/locations', label: 'Endereços', icon: <LocationOnIcon /> },
  { href: '/vehicles', label: 'Veículos', icon: <DirectionsCarIcon /> },
  { href: '/deliveries', label: 'Encomendas', icon: <LocalShippingIcon /> },
]

export default function Layout({ children }) {
  const theme = useTheme()
  const [open, setOpen] = React.useState(true) // Desktop state
  const [mobileOpen, setMobileOpen] = React.useState(false) // Mobile state
  const router = useRouter()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const handleDrawerOpen = () => {
    setOpen(true)
  }

  const handleDrawerClose = () => {
    setOpen(false)
  }

  const drawerContent = (isDesktop) => (
    <>
      <DrawerHeader>
        <Typography variant="subtitle1" sx={{ flexGrow: 1, ml: 2, fontWeight: 700, color: 'white' }}>
          Distribuição
        </Typography>
        {isDesktop && (
          <IconButton onClick={handleDrawerClose} sx={{ color: 'white' }} aria-label="close drawer">
            {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
        )}
      </DrawerHeader>
      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />
      <List>
        {navLinks.map((link) => {
          const isActive = router.pathname === link.href || (link.href !== '/' && router.pathname.startsWith(link.href))
          return (
            <ListItem key={link.href} disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => {
                  router.push(link.href)
                  if (!isDesktop) setMobileOpen(false)
                }}
                sx={{
                  minHeight: 48,
                  justifyContent: (isDesktop && !open) ? 'center' : 'initial',
                  px: 2.5,
                  backgroundColor: isActive ? 'rgba(255,255,255,0.08)' : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.12)',
                  },
                  borderLeft: isActive ? `4px solid ${theme.palette.primary.main}` : '4px solid transparent',
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: (isDesktop && !open) ? 'auto' : 3,
                    justifyContent: 'center',
                    color: isActive ? theme.palette.primary.main : 'rgba(255,255,255,0.7)',
                  }}
                >
                  {link.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={link.label} 
                  sx={{ 
                    opacity: (isDesktop && !open) ? 0 : 1,
                    '& span': {
                      fontWeight: isActive ? 600 : 400,
                      color: isActive ? 'white' : 'rgba(255,255,255,0.85)'
                    }
                  }} 
                />
              </ListItemButton>
            </ListItem>
          )
        })}
      </List>
    </>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      {/* Mobile AppBar */}
      <MuiAppBar
        position="fixed"
        sx={{
          display: { xs: 'block', sm: 'none' },
          backgroundColor: theme.palette.background.paper,
          color: theme.palette.text.primary,
          boxShadow: 'none',
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 600 }}>
            Planejamento Rota
          </Typography>
        </Toolbar>
      </MuiAppBar>

      {/* Desktop AppBar */}
      <AppBarDesktop 
        position="fixed" 
        open={open}
        sx={{ display: { xs: 'none', sm: 'block' } }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{
              marginRight: 5,
              ...(open && { display: 'none' }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 600 }}>
            Planejamento de Rotas
          </Typography>
        </Toolbar>
      </AppBarDesktop>

      {/* Mobile Drawer */}
      <MuiDrawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: drawerWidth,
            backgroundColor: theme.palette.secondary.main,
            color: theme.palette.secondary.contrastText,
          },
        }}
      >
        {drawerContent(false)}
      </MuiDrawer>

      {/* Desktop Drawer */}
      <DrawerDesktop 
        variant="permanent" 
        open={open}
        sx={{ display: { xs: 'none', sm: 'block' } }}
      >
        {drawerContent(true)}
      </DrawerDesktop>

      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, sm: 3 }, pt: { xs: 10, sm: 10 }, width: '100%' }}>
        {children}
      </Box>
    </Box>
  )
}
