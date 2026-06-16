<template>
  <main class="flex min-h-screen bg-background font-sans text-foreground selection:bg-primary-fixed selection:text-on-primary-fixed overflow-x-hidden">
    <!-- Left Side: Registration Form -->
    <section class="w-full lg:w-1/2 bg-surface-container-lowest flex flex-col justify-center items-center px-6 py-16 relative">
      <div class="absolute top-8 left-8 flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-[32px]" style="font-variation-settings: 'FILL' 1;">analytics</span>
        <span class="text-2xl text-primary font-bold tracking-tight">ResumeAI</span>
      </div>
      <div class="w-full max-w-[400px] flex flex-col gap-8">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold text-on-surface">Create your account</h1>
          <p class="text-on-surface-variant text-base">
            Already have an account? 
            <NuxtLink to="/login" class="text-primary font-bold hover:underline">Sign in</NuxtLink>
          </p>
        </div>

        <Alert variant="destructive" v-if="errorMessage">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{{ errorMessage }}</AlertDescription>
        </Alert>

        <!-- Google OAuth -->
        <button class="w-full flex items-center justify-center gap-2 py-2 px-4 border border-outline-variant rounded-lg bg-white text-on-surface-variant font-semibold text-sm hover:bg-surface-container-low transition-colors active:scale-95 duration-200">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
          </svg>
          Continue with Google
        </button>

        <div class="flex items-center gap-4">
          <div class="h-px bg-outline-variant/30 flex-1"></div>
          <span class="text-xs text-outline uppercase tracking-widest">or email</span>
          <div class="h-px bg-outline-variant/30 flex-1"></div>
        </div>

        <form @submit.prevent="onSubmit" class="flex flex-col gap-4">
          <div class="space-y-1">
            <Label for="email" class="font-semibold text-on-surface-variant">Email Address</Label>
            <Input 
              id="email" 
              type="email" 
              placeholder="alex@example.com" 
              v-model="email" 
              v-bind="emailProps"
              :class="['w-full px-4 py-2 rounded-lg border border-outline-variant bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base text-on-surface', {'border-destructive focus:ring-destructive/20 focus:border-destructive': errors.email}]" 
            />
            <p class="text-sm font-medium text-destructive mt-1" v-if="errors.email">{{ errors.email }}</p>
          </div>
          
          <div class="space-y-1">
            <Label for="password" class="font-semibold text-on-surface-variant">Password</Label>
            <div class="relative group">
              <Input 
                id="password" 
                :type="showPassword ? 'text' : 'password'" 
                placeholder="••••••••" 
                v-model="password" 
                v-bind="passwordProps"
                @input="calculateStrength"
                :class="['w-full px-4 py-2 rounded-lg border border-outline-variant bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base text-on-surface pr-10', {'border-destructive focus:ring-destructive/20 focus:border-destructive': errors.password}]" 
              />
              <button 
                type="button" 
                class="absolute right-2 top-1/2 -translate-y-1/2 text-outline-variant hover:text-primary transition-colors p-1"
                @click="showPassword = !showPassword"
              >
                <span class="material-symbols-outlined text-[20px]">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
              </button>
            </div>
            
            <!-- Password Strength Bar -->
            <div class="flex gap-1 mt-2 h-1.5">
              <div v-for="n in 4" :key="n" :class="getStrengthClass(n)"></div>
            </div>
            <p class="text-sm font-medium text-destructive mt-1" v-if="errors.password">{{ errors.password }}</p>
          </div>

          <div class="space-y-1 mt-2">
            <Label for="confirm-password" class="font-semibold text-on-surface-variant">Confirm Password</Label>
            <div class="relative">
              <Input 
                id="confirm-password" 
                :type="showConfirmPassword ? 'text' : 'password'" 
                placeholder="••••••••" 
                v-model="confirmPassword" 
                v-bind="confirmPasswordProps"
                :class="['w-full px-4 py-2 rounded-lg border border-outline-variant bg-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-base text-on-surface pr-10', {'border-destructive focus:ring-destructive/20 focus:border-destructive': errors.confirmPassword}]" 
              />
              <button 
                type="button" 
                class="absolute right-2 top-1/2 -translate-y-1/2 text-outline-variant hover:text-primary transition-colors p-1"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <span class="material-symbols-outlined text-[20px]">{{ showConfirmPassword ? 'visibility_off' : 'visibility' }}</span>
              </button>
            </div>
            <p class="text-sm font-medium text-destructive mt-1" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</p>
          </div>

          <p class="text-sm text-on-surface-variant/70 mt-2">
            By creating an account, you agree to our <a class="text-primary hover:underline" href="#">Terms of Service</a> and <a class="text-primary hover:underline" href="#">Privacy Policy</a>.
          </p>

          <Button class="w-full py-4 px-6 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 transition-all active:scale-[0.98] shadow-md shadow-primary/20 mt-2 h-auto" type="submit" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Creating Account...
            </span>
            <span v-else>Create Account</span>
          </Button>
        </form>
      </div>
    </section>

    <!-- Right Side: Decorative/Preview -->
    <section class="hidden lg:flex w-1/2 bg-gradient-to-br from-primary to-[#8b5cf6] relative overflow-hidden items-center justify-center">
      <!-- Animated Background Detail -->
      <div class="absolute inset-0 opacity-20"></div>
      
      <div class="relative z-10 w-full max-w-[500px] px-8">
        <!-- Floating Card UI -->
        <div class="animate-[float_6s_ease-in-out_infinite] bg-white rounded-2xl shadow-2xl p-8 border border-white/20 backdrop-blur-sm bg-white/95">
          <div class="flex justify-between items-start mb-6">
            <div class="space-y-1">
              <span class="text-xs font-bold text-primary uppercase tracking-widest">Analysis Preview</span>
              <h3 class="text-2xl font-semibold text-on-surface">Senior Product Designer</h3>
            </div>
            <div class="w-16 h-16 rounded-full border-[6px] border-surface-container flex items-center justify-center relative">
              <svg class="absolute inset-0 -rotate-90 w-full h-full" viewBox="0 0 64 64">
                <circle cx="32" cy="32" fill="none" r="26" stroke="#e0d2ff" stroke-width="6"></circle>
                <circle cx="32" cy="32" fill="none" r="26" stroke="#4f378a" stroke-dasharray="163.36" stroke-dashoffset="29.4" stroke-width="6" stroke-linecap="round"></circle>
              </svg>
              <span class="font-bold text-primary text-base">82%</span>
            </div>
          </div>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between text-on-surface-variant border-b border-outline-variant/20 pb-2">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[#10b981] text-[20px]" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                <span class="text-base">Quantified Achievements</span>
              </div>
              <span class="text-sm font-bold text-[#10b981]">+15</span>
            </div>
            <div class="flex items-center justify-between text-on-surface-variant border-b border-outline-variant/20 pb-2">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[#10b981] text-[20px]" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                <span class="text-base">Keyword Optimization</span>
              </div>
              <span class="text-sm font-bold text-[#10b981]">+12</span>
            </div>
            <div class="flex items-center justify-between text-on-surface-variant border-b border-outline-variant/20 pb-2">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[#f59e0b] text-[20px]" style="font-variation-settings: 'FILL' 1;">info</span>
                <span class="text-base">Formatting & Layout</span>
              </div>
              <span class="text-sm font-bold text-[#f59e0b]">-4</span>
            </div>
            <div class="flex items-center justify-between text-on-surface-variant">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[#ef4444] text-[20px]" style="font-variation-settings: 'FILL' 1;">error</span>
                <span class="text-base">Action Verb Strength</span>
              </div>
              <span class="text-sm font-bold text-[#ef4444]">-10</span>
            </div>
          </div>
          
          <div class="mt-8 pt-6 border-t border-outline-variant/20">
            <p class="text-on-surface-variant text-base italic leading-relaxed">
              "Your experience with React and Design Systems is highly relevant. Consider quantifying the 'user engagement' increase in your second role."
            </p>
          </div>
        </div>
        
        <!-- Descriptive Image -->
        <div class="mt-16 text-center">
          <img class="rounded-xl shadow-lg border border-white/10 opacity-80 mix-blend-screen max-w-[400px] mx-auto" alt="Workspace scene" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCkl5eqvP5CxGuFUvxrF7-LPQNhtpv7ERBxWudD856g-77XSGTlm3fkD7AocuA9qaayLNMhw6F7aucuvmfsnF9nxsG3Vk5vggFSOVAq9o15oPx8ENPW972e4e3XWziqPn2FT4xQ8oah5esNh6_s8yHcanAzJMgL5HzJcr5CZ-GyabCLDGwl3qlVobSvyrkzlYkXrBKqlwkU9mLWf0VUy2L7q-3dxVgw3KSX2fsVlF_aEBiVXU0SCaZWRcouNlgwtsZbQCW3rTAHyP4">
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { useAuth } from '~/composables/useAuth'

import { Input } from '~/components/ui/input/index'
import { Label } from '~/components/ui/label/index'
import { Button } from '~/components/ui/button/index'
import { Alert, AlertTitle, AlertDescription } from '~/components/ui/alert/index'

definePageMeta({
  layout: false,
  middleware: 'guest'
})

const { register } = useAuth()
const errorMessage = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const passwordStrength = ref(0)

const formSchema = toTypedSchema(z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
}))

const { handleSubmit, defineField, errors, isSubmitting } = useForm({
  validationSchema: formSchema,
})

const [email, emailProps] = defineField('email')
const [password, passwordProps] = defineField('password')
const [confirmPassword, confirmPasswordProps] = defineField('confirmPassword')

const calculateStrength = () => {
  const val = password.value || ''
  let strength = 0
  if (val.length > 0) strength = 1
  if (val.length > 5) strength = 2
  if (val.length > 8 && /[A-Z]/.test(val)) strength = 3
  if (val.length > 10 && /[!@#$%^&*]/.test(val)) strength = 4
  passwordStrength.value = strength
}

const getStrengthClass = (index: number) => {
  if (index <= passwordStrength.value) {
    if (passwordStrength.value === 1) return 'h-full flex-1 rounded-full bg-error transition-all duration-300'
    if (passwordStrength.value === 2) return 'h-full flex-1 rounded-full bg-tertiary transition-all duration-300'
    if (passwordStrength.value === 3) return 'h-full flex-1 rounded-full bg-emerald-400 transition-all duration-300'
    if (passwordStrength.value === 4) return 'h-full flex-1 rounded-full bg-emerald-600 transition-all duration-300'
  }
  return 'h-full flex-1 rounded-full bg-outline-variant/20 transition-all duration-300'
}

const onSubmit = handleSubmit(async (values) => {
  errorMessage.value = ''
  const result = await register({
    email: values.email,
    password: values.password
  })
  
  if (!result.success) {
    errorMessage.value = result.error
  }
})
</script>
