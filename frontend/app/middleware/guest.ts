import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = useAuthStore()
  const token = useCookie('access_token', { path: '/' })

  // If there's a token but the user is not in the store (e.g. after refresh),
  // we try to fetch the user profile.
  if (token.value && !authStore.isAuthenticated) {
    const { fetchMe } = useAuth()
    await fetchMe()
  }

  // If authenticated, redirect away from guest-only pages
  if (authStore.isAuthenticated) {
    return navigateTo('/dashboard')
  }
})
