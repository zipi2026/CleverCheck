import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { User } from '../models/User'
import type { LoginPayload, AuthResponse } from '../services/authService'
import { login as loginRequest, logout as logoutRequest } from '../services/authService'

interface AuthContextValue {
  user: User | null
  token: string | null
  signIn: (payload: LoginPayload) => Promise<User>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

const AUTH_USER_KEY = 'clevercheck_auth_user'
const AUTH_TOKEN_KEY = 'clevercheck_auth_token'

function getStoredUser(): User | null {
  if (typeof window === 'undefined') return null
  const raw = window.localStorage.getItem(AUTH_USER_KEY)
  return raw ? JSON.parse(raw) as User : null
}

function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null
  return window.localStorage.getItem(AUTH_TOKEN_KEY)
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    setUser(getStoredUser())
    setToken(getStoredToken())
  }, [])

  const signIn = useCallback(async (payload: LoginPayload) => {
    const auth = await loginRequest(payload)
    setUser(auth.user)
    setToken(auth.token)
    window.localStorage.setItem(AUTH_USER_KEY, JSON.stringify(auth.user))
    window.localStorage.setItem(AUTH_TOKEN_KEY, auth.token)
    return auth.user
  }, [])

  const signOut = useCallback(async () => {
    await logoutRequest(token ?? undefined)
    setUser(null)
    setToken(null)
    window.localStorage.removeItem(AUTH_USER_KEY)
    window.localStorage.removeItem(AUTH_TOKEN_KEY)
  }, [token])

  const value = useMemo(
    () => ({ user, token, signIn, signOut }),
    [user, token, signIn, signOut],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
