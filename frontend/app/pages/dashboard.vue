<template>
  <div class="w-full">
    <!-- MOBILE LAYOUT -->
    <div class="md:hidden block space-y-6">
      <!-- Welcome Header -->
      <section class="mt-4">
        <h1 class="font-headline-lg-mobile text-headline-lg-mobile text-on-surface">Hello, Alex</h1>
        <p class="font-body-sm text-body-sm text-on-surface-variant">Your career progression is on track.</p>
      </section>

      <!-- Stats Chips - Horizontal Scroll -->
      <section class="flex gap-2 overflow-x-auto no-scrollbar -mx-4 px-4 py-1">
        <div class="flex-none bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 min-w-[130px] shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
          <span class="font-label-sm text-label-sm text-on-surface-variant block mb-1">Analyses</span>
          <span class="font-headline-sm text-headline-sm font-bold text-primary">{{ totalAnalyses }}</span>
        </div>
        <div class="flex-none bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 min-w-[130px] shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
          <span class="font-label-sm text-label-sm text-on-surface-variant block mb-1">Avg Score</span>
          <span class="font-headline-sm text-headline-sm font-bold text-tertiary">{{ avgScore }}%</span>
        </div>
        <div class="flex-none bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 min-w-[130px] shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
          <span class="font-label-sm text-label-sm text-on-surface-variant block mb-1">Best Score</span>
          <span class="font-headline-sm text-headline-sm font-bold text-primary-container text-on-primary-container inline-block px-2 rounded-md">{{ bestScore }}%</span>
        </div>
      </section>

      <!-- Primary CTA -->
      <section>
        <NuxtLink to="/analyze">
          <button class="w-full bg-primary py-4 rounded-xl flex items-center justify-center gap-2 !text-white font-label-md text-label-md active:scale-[0.98] transition-transform active:opacity-90 shadow-md">
            <span class="material-symbols-outlined">add_circle</span>
            New Analysis
          </button>
        </NuxtLink>
      </section>

      <!-- Analysis List Header -->
      <section class="flex items-center justify-between">
        <h2 class="font-headline-sm text-headline-sm text-on-surface">Recent Analyses</h2>
        <button class="font-label-sm text-label-sm text-primary">See all</button>
      </section>

      <!-- Analysis List -->
      <section class="space-y-4" v-if="hasAnalyses">
        <div v-for="analysis in analyses" :key="analysis.id" @click="navigateToResult(analysis.id)" class="bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 flex items-center gap-4 shadow-[0_1px_3px_rgba(0,0,0,0.08)] active:bg-surface-variant/20 transition-colors cursor-pointer">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center" :class="getScoreColorClass(analysis.match_score, 'bg').replace('text', 'bg').replace('500', '100') + ' ' + getScoreTextClass(analysis.match_score)">
            <span class="material-symbols-outlined text-[28px]">{{ analysis.match_score >= 80 ? 'description' : analysis.match_score >= 60 ? 'history' : 'warning' }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-label-md text-label-md text-on-surface truncate">{{ analysis.label || 'Untitled Analysis' }}</h3>
            <p class="font-body-sm text-body-sm text-on-surface-variant">{{ formatDate(analysis.created_at) }}</p>
          </div>
          <div class="text-right">
            <div class="font-headline-sm text-headline-sm font-bold" :class="getScoreTextClass(analysis.match_score)">{{ Math.round(analysis.match_score) }}%</div>
            <span class="font-label-sm text-label-sm text-on-surface-variant">Score</span>
          </div>
        </div>
      </section>
      
      <!-- Empty State Filler / Encouragement -->
      <section v-else class="pt-8 pb-12 text-center space-y-2">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-surface-container-high text-on-surface-variant">
          <span class="material-symbols-outlined text-[32px]">auto_awesome</span>
        </div>
        <h4 class="font-headline-sm text-headline-sm text-on-surface">Unlock Insights</h4>
        <p class="font-body-sm text-body-sm text-on-surface-variant max-w-[240px] mx-auto">Upload a new resume to see how you match against current job descriptions.</p>
      </section>
    </div>

    <!-- DESKTOP LAYOUT -->
    <div class="hidden md:block">
      <!-- Header Section -->
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-md mb-12">
        <div>
          <h1 class="font-headline-lg text-headline-lg text-on-surface">My Analyses</h1>
          <p class="font-body-lg text-body-lg text-on-surface-variant">Track how your resumes perform in real-time.</p>
        </div>
        <NuxtLink to="/analyze">
          <Button class="bg-primary !text-white px-6 py-2 h-auto rounded-lg font-label-md text-label-md flex items-center gap-2 hover:bg-primary/90 active:scale-95 transition-all shadow-md">
            <span class="material-symbols-outlined text-[20px]">add</span>
            New Analysis
          </Button>
        </NuxtLink>
      </div>

      <!-- Empty State -->
      <section v-if="!hasAnalyses" class="flex flex-col items-center justify-center min-h-[60vh] py-12" id="empty-state">
        <div class="relative mb-8">
          <div class="w-64 h-64 bg-surface-container-low rounded-full flex items-center justify-center animate-float">
            <div class="relative">
              <span class="material-symbols-outlined text-[80px] text-outline-variant/40">description</span>
              <div class="absolute -bottom-2 -right-4 bg-primary-fixed p-4 rounded-2xl shadow-lg border border-white">
                <span class="material-symbols-outlined text-primary text-[32px]">search</span>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center space-y-4 max-w-md">
          <h1 class="font-headline-lg text-headline-lg text-on-surface">No analyses yet</h1>
          <p class="font-body-lg text-body-lg text-on-surface-variant">Upload your resume and a job description to get started with your first AI-powered match analysis.</p>
          <div class="pt-4">
            <NuxtLink to="/analyze">
              <Button class="bg-primary !text-white px-8 py-6 h-auto rounded-lg font-label-md text-label-md hover:bg-primary/90 transition-all flex items-center gap-2 mx-auto shadow-lg hover:-translate-y-0.5">
                <span class="material-symbols-outlined">add_circle</span>
                Analyze My Resume
              </Button>
            </NuxtLink>
          </div>
        </div>
      </section>

      <!-- Populated State -->
      <template v-else>
        <!-- Stats Row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <!-- Stat 1 -->
          <Card class="bg-white border-outline-variant/30 p-6 rounded-xl shadow-[0_1px_3px_rgba(0,0,0,0.08)] flex items-center gap-6 border-0 ring-1 ring-outline-variant/30">
            <div class="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center text-primary">
              <span class="material-symbols-outlined">analytics</span>
            </div>
            <div>
              <p class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">Total Analyses</p>
              <p class="text-2xl font-bold text-on-surface">{{ totalAnalyses }}</p>
            </div>
          </Card>
          
          <!-- Stat 2 -->
          <Card class="bg-white border-outline-variant/30 p-6 rounded-xl shadow-[0_1px_3px_rgba(0,0,0,0.08)] flex items-center gap-6 border-0 ring-1 ring-outline-variant/30">
            <div class="w-12 h-12 rounded-full bg-secondary-container flex items-center justify-center text-secondary">
              <span class="material-symbols-outlined">trending_up</span>
            </div>
            <div>
              <p class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">Average Score</p>
              <p class="text-2xl font-bold text-on-surface">{{ avgScore }}%</p>
            </div>
          </Card>
          
          <!-- Stat 3 -->
          <Card class="bg-white border-outline-variant/30 p-6 rounded-xl shadow-[0_1px_3px_rgba(0,0,0,0.08)] flex items-center gap-6 border-0 ring-1 ring-outline-variant/30">
            <div class="w-12 h-12 rounded-full bg-tertiary-fixed flex items-center justify-center text-tertiary">
              <span class="material-symbols-outlined">military_tech</span>
            </div>
            <div>
              <p class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">Best Score</p>
              <p class="text-2xl font-bold text-on-surface">{{ bestScore }}%</p>
            </div>
          </Card>
        </div>

        <!-- Analysis List -->
        <div class="space-y-4">
          <div v-for="analysis in analyses" :key="analysis.id" class="bg-white/80 backdrop-blur-md group border border-outline-variant/30 p-6 rounded-xl hover:border-primary/50 transition-all flex flex-col md:flex-row items-center justify-between gap-6 hover:-translate-y-0.5 duration-300 cursor-pointer" @click="navigateToResult(analysis.id)">
            <div class="flex items-center gap-6 w-full md:w-auto">
              <div class="relative w-16 h-16 flex items-center justify-center">
                <svg class="w-full h-full -rotate-90" viewBox="0 0 64 64">
                  <circle class="text-outline-variant/20" cx="32" cy="32" fill="transparent" r="28" stroke="currentColor" stroke-width="4"></circle>
                  <circle :class="getScoreColorClass(analysis.match_score, 'text')" cx="32" cy="32" fill="transparent" r="28" stroke="currentColor" stroke-dasharray="175.93" :stroke-dashoffset="175.93 - (175.93 * analysis.match_score / 100)" stroke-width="4" stroke-linecap="round"></circle>
                </svg>
                <span class="absolute font-bold" :class="getScoreTextClass(analysis.match_score)">{{ Math.round(analysis.match_score) }}%</span>
              </div>
              <div>
                <h3 class="text-lg font-bold text-on-surface mb-1">{{ analysis.label || 'Untitled Analysis' }}</h3>
                <p class="text-sm text-on-surface-variant">{{ formatDate(analysis.created_at) }} · <span class="font-bold" :class="getScoreTextClass(analysis.match_score)">{{ analysis.match_score > 70 ? 'Good Match' : 'Needs Improvement' }}</span></p>
              </div>
            </div>
            <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
              <Button variant="ghost" class="text-primary font-bold flex items-center gap-1 hover:bg-primary-fixed/30 px-4 py-2 h-auto rounded-lg transition-colors" @click.stop="navigateToResult(analysis.id)">
                View <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
              </Button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="mt-12 flex flex-col md:flex-row items-center justify-between border-t border-outline-variant/20 pt-6 gap-4">
          <p class="text-sm text-on-surface-variant">Showing 4 of 12 analyses</p>
          <div class="flex items-center gap-2">
            <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant/30 text-on-surface-variant hover:bg-surface-variant/50 transition-all">
              <span class="material-symbols-outlined">chevron_left</span>
            </button>
            <button class="w-10 h-10 flex items-center justify-center rounded-lg bg-primary text-white font-bold">1</button>
            <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant/30 text-on-surface-variant hover:bg-surface-variant/50 transition-all">2</button>
            <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant/30 text-on-surface-variant hover:bg-surface-variant/50 transition-all">3</button>
            <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-outline-variant/30 text-on-surface-variant hover:bg-surface-variant/50 transition-all">
              <span class="material-symbols-outlined">chevron_right</span>
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Card } from '~/components/ui/card/index'
import { Button } from '~/components/ui/button/index'
import { useAnalysis } from '~/composables/useAnalysis'
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  middleware: 'auth'
})

const router = useRouter()
const authStore = useAuthStore()
const { fetchHistory } = useAnalysis()

const analyses = ref<any[]>([])
const isLoading = ref(true)
const totalAnalyses = ref(0)
const currentPage = ref(1)

const hasAnalyses = computed(() => analyses.value.length > 0)

const avgScore = computed(() => {
  if (analyses.value.length === 0) return 0
  const total = analyses.value.reduce((acc, curr) => acc + curr.match_score, 0)
  return Math.round(total / analyses.value.length)
})

const bestScore = computed(() => {
  if (analyses.value.length === 0) return 0
  return Math.max(...analyses.value.map(a => a.match_score))
})

const loadAnalyses = async (page = 1) => {
  isLoading.value = true
  const result = await fetchHistory(page, 10)
  if (result.success && result.data) {
    analyses.value = result.data.items || []
    totalAnalyses.value = result.data.total || 0
    currentPage.value = page
  }
  isLoading.value = false
}

onMounted(() => {
  loadAnalyses()
})

const navigateToResult = (id: string) => {
  router.push(`/result?id=${id}`)
}

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const getScoreColorClass = (score: number, prefix: string) => {
  if (score >= 80) return `${prefix}-emerald-500`
  if (score >= 60) return `${prefix}-amber-500`
  return `${prefix}-error`
}

const getScoreTextClass = (score: number) => {
  if (score >= 80) return `text-emerald-700`
  if (score >= 60) return `text-amber-700`
  return `text-error`
}
</script>

<style scoped>
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}
</style>
