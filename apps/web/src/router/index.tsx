import { createBrowserRouter } from 'react-router-dom'

/**
 * React Router configuration for Omnipresence.
 */
export const router = createBrowserRouter([
  {
    path: '/',
    element: <div>Dashboard</div>,
  },
  {
    path: '/login',
    element: <div>Login</div>,
  },
  {
    path: '/participants',
    element: <div>Participants</div>,
  },
  {
    path: '/groups',
    element: <div>Groups</div>,
  },
  {
    path: '/sessions',
    element: <div>Sessions</div>,
  },
  {
    path: '/sessions/:id',
    element: <div>Session Detail</div>,
  },
  {
    path: '/reports',
    element: <div>Reports</div>,
  },
  {
    path: '/admin',
    element: <div>Admin</div>,
  },
])
