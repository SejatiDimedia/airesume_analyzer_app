<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '~/utils/utils'

interface Props {
  modelValue?: string | number
  type?: string
  placeholder?: string
  disabled?: boolean
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
}>()

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const inputClass = computed(() => {
  return cn(
    'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-ring focus-visible:shadow-[0_0_0_2px_rgba(79,55,138,0.1)] disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200',
    props.class
  )
})
</script>

<template>
  <input
    :type="type"
    :value="modelValue"
    @input="onInput"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="inputClass"
  />
</template>
