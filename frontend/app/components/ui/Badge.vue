<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '~/utils/utils'

interface Props {
  variant?: 'default' | 'secondary' | 'success' | 'warning' | 'destructive' | 'outline'
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
})

const variantClasses = {
  default: 'bg-primary text-primary-foreground hover:bg-primary/80',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
  success: 'bg-[#e1f0e5] text-[#1e6037]', // Emerald matching
  warning: 'bg-[#fdf3db] text-[#8e6200]', // Amber matching
  destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/80',
  outline: 'border border-input bg-background text-foreground',
}

const badgeClass = computed(() => {
  return cn(
    'inline-flex items-center rounded-md px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
    variantClasses[props.variant],
    props.class
  )
})
</script>

<template>
  <div :class="badgeClass">
    <slot />
  </div>
</template>
