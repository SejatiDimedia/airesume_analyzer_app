<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '~/utils/utils'

interface Props {
  variant?: 'default' | 'secondary' | 'ai' | 'destructive' | 'outline' | 'ghost'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  disabled?: boolean
  as?: string
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'default',
  disabled: false,
  as: 'button',
})

const variantClasses = {
  default: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
  ai: 'bg-gradient-to-r from-primary to-accent-foreground text-primary-foreground hover:opacity-90',
  destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
  outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
  ghost: 'hover:bg-accent hover:text-accent-foreground',
}

const sizeClasses = {
  default: 'h-10 px-4 py-2',
  sm: 'h-9 rounded-md px-3',
  lg: 'h-11 rounded-md px-8',
  icon: 'h-10 w-10',
}

const buttonClass = computed(() => {
  return cn(
    'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
    variantClasses[props.variant],
    sizeClasses[props.size],
    props.class
  )
})
</script>

<template>
  <component :is="as" :class="buttonClass" :disabled="disabled">
    <slot />
  </component>
</template>
