<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { cn } from '~/utils/utils'

interface Props {
  score: number
  size?: number
  strokeWidth?: number
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 120,
  strokeWidth: 8,
})

const currentScore = ref(0)

onMounted(() => {
  // Animate score from 0 to target
  setTimeout(() => {
    currentScore.value = props.score
  }, 100)
})

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => radius.value * 2 * Math.PI)
const strokeDashoffset = computed(() => 
  circumference.value - (currentScore.value / 100) * circumference.value
)

const colorClass = computed(() => {
  if (currentScore.value >= 75) return 'text-[#10b981]' // Emerald 500
  if (currentScore.value >= 50) return 'text-[#f59e0b]' // Amber 500
  return 'text-[#ef4444]' // Red 500
})
</script>

<template>
  <div :class="cn('relative flex items-center justify-center', props.class)" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg
      class="transform -rotate-90"
      :width="size"
      :height="size"
    >
      <!-- Background Circle -->
      <circle
        class="text-muted"
        stroke-width="strokeWidth"
        stroke="currentColor"
        fill="transparent"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
      />
      <!-- Progress Circle -->
      <circle
        :class="['transition-all duration-1000 ease-out', colorClass]"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
        stroke-linecap="round"
        stroke="currentColor"
        fill="transparent"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
      />
    </svg>
    <div class="absolute flex flex-col items-center justify-center">
      <span class="text-3xl font-bold font-sans tracking-tighter" :class="colorClass">
        {{ Math.round(currentScore) }}
      </span>
      <span class="text-xs text-muted-foreground font-medium uppercase tracking-wider">Score</span>
    </div>
  </div>
</template>
