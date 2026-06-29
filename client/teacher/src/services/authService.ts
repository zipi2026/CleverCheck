import { SERVER_URL } from '../config'
import type { User } from '../models/User'

export interface LoginPayload {
  username: string
  password: string
}

export interface AuthResponse {
  user: User
  token: string
}

const loginUrl = `${SERVER_URL}/auth/login`
const logoutUrl = `${SERVER_URL}/auth/logout`

async function handleJsonResponse<T>(response: Response): Promise<T> {
  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    const message = payload?.message || response.statusText || 'Authentication request failed.'
    throw new Error(String(message))
  }

  return payload as T
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  const response = await fetch(loginUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  return handleJsonResponse<AuthResponse>(response)
}

export async function logout(token?: string): Promise<void> {
  await fetch(logoutUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })
}
