/**
 * Zustand store for authentication state management.
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  isAuthenticated: boolean
  user: User | null
  token: string | null
  setAuth: (user: User, token: string) => void
  clearAuth: () => void
}

interface User {
  id: number
  email: string
  role: string
  organization: {
    id: number
    name: string
    slug: string
    domain_type: string
  }
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      user: null,
      token: null,
      setAuth: (user, token) => {
        set({ isAuthenticated: true, user, token })
        localStorage.setItem('auth_token', token)
      },
      clearAuth: () => {
        set({ isAuthenticated: false, user: null, token: null })
        localStorage.removeItem('auth_token')
      },
    }),
    {
      name: 'omnipresence-auth',
    }
  )
)
