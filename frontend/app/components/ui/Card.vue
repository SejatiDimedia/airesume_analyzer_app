<script setup lang="ts">
import { cn } from '~/utils/utils'

interface Props {
  class?: string
}

const props = defineProps<Props>()
</script>

<template>
  <div :class="cn('rounded-xl border border-border bg-card text-card-foreground shadow-sm', props.class)">
    <slot />
  </div>
</template>
