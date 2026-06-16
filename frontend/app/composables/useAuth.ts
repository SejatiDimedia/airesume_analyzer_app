import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'
import { useCookie, useRuntimeConfig } from '#app'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const config = useRuntimeConfig()
  
  // Create a reusable fetch instance that automatically attaches the bearer token
  const apiFetch = $fetch.create({
    baseURL: config.public.apiBaseUrl as string,
    onRequest({ options }) {
      const token = useCookie('access_token', { path: '/' }).value
      if (token) {
        options.headers = new Headers(options.headers || {})
        options.headers.set('Authorization', `Bearer ${token}`)
      }
    }
  })

  const login = async (data: any) => {
    const formData = new URLSearchParams()
    formData.append('grant_type', 'password')
    formData.append('username', data.email)
    formData.append('password', data.password)

    try {
      const res: any = await $fetch(`${config.public.apiBaseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
      })
      
      const tokenCookie = useCookie('access_token', { maxAge: 60 * 60 * 24 * 7, path: '/' })
      tokenCookie.value = res.access_token
      
      await fetchMe()
      router.push('/dashboard')
      return { success: true }
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.response?._data?.detail || error.message }
    }
  }

  const register = async (data: any) => {
    try {
      await $fetch(`${config.public.apiBaseUrl}/auth/register`, {
        method: 'POST',
        body: data
      })
      // Auto login after register
      return await login(data)
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.response?._data?.error?.message || error.message }
    }
  }

  const fetchMe = async () => {
    const token = useCookie('access_token', { path: '/' }).value
    if (!token) {
      authStore.clearUser()
      return
    }
    try {
      const user = await apiFetch('/auth/me')
      authStore.setUser(user)
    } catch (error) {
      authStore.clearUser()
      useCookie('access_token', { path: '/' }).value = null
    }
  }

  const logout = () => {
    useCookie('access_token', { path: '/' }).value = null
    authStore.clearUser()
    router.push('/login')
  }

  return {
    login,
    register,
    fetchMe,
    logout,
    apiFetch
  }
}
