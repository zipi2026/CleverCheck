import { useState } from 'react'
import { /* Link as RouterLink, */ useNavigate } from 'react-router-dom'
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Alert,
  Box,
  Button,
  Container,
  /* Link, */
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import { useAuth } from '../context/AuthContext'

const loginSchema = z.object({
  username: z.string().min(1, 'Username is required'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginFormValues = z.infer<typeof loginSchema>

export default function LoginPage() {
  const [serverError, setServerError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { signIn } = useAuth()

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = async (values: LoginFormValues) => {
    setServerError(null)

    try {
      await signIn(values)
      navigate('/')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed. Please try again.'
      setServerError(message)
    }
  }

  return (
    <Container maxWidth="xs" sx={{ py: 6 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Stack spacing={3}>
          <Box>
            <Typography component="h1" variant="h5" gutterBottom>
              Student / Teacher Login
            </Typography>
            <Typography color="text.secondary" variant="body2">
              Enter your email and password to access CleverCheck.
            </Typography>
          </Box>

          {serverError ? <Alert severity="error">{serverError}</Alert> : null}

          <Box component="form" noValidate onSubmit={handleSubmit(onSubmit)}>
            <Stack spacing={2}>
              <Controller
                name="username"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Username"
                    type="text"
                    required
                    fullWidth
                    error={Boolean(errors.username)}
                    helperText={errors.username?.message}
                  />
                )}
              />

              <Controller
                name="password"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Password"
                    type="password"
                    required
                    fullWidth
                    error={Boolean(errors.password)}
                    helperText={errors.password?.message}
                  />
                )}
              />

              <Button type="submit" variant="contained" size="large" disabled={isSubmitting}>
                Sign in
              </Button>
            </Stack>
          </Box>

          {/*
          <Typography variant="body2" color="text.secondary">
            Need an account?{' '}
            <Link component={RouterLink} to="/register">
              Register
            </Link>
          </Typography>
          */}
        </Stack>
      </Paper>
    </Container>
  )
}
