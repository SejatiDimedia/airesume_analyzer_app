<template>
  <div class="px-4 md:px-8 max-w-container_max mx-auto min-h-screen pt-8 pb-32">
    <div v-if="isLoading" class="flex justify-center items-center h-[60vh]">
      <span class="material-symbols-outlined animate-spin text-primary text-4xl">sync</span>
    </div>
    <div v-else-if="analysis">
      <!-- Breadcrumbs -->
      <div class="flex items-center gap-1 mb-8 animate-fade-in">
        <NuxtLink to="/dashboard" class="text-on-surface-variant hover:text-primary transition-colors font-label-md text-label-md">
          My Analyses
        </NuxtLink>
        <span class="material-symbols-outlined text-outline-variant text-[18px]">chevron_right</span>
        <span class="text-primary font-bold font-label-md text-label-md">{{ analysis.label || 'Untitled Analysis' }}</span>
      </div>
      
      <!-- 2-Column Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left Column (60%) -->
        <div class="lg:col-span-7 flex flex-col gap-6">
          
          <!-- Score Card -->
          <Card class="bg-white border-outline-variant/30 rounded-xl p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)] animate-fade-in border-0 ring-1 ring-outline-variant/30" style="animation-delay: 0.1s;">
            <div class="flex flex-col md:flex-row items-center gap-8">
              <div class="relative w-[120px] h-[120px] flex items-center justify-center shrink-0">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle class="text-surface-container-high" cx="50" cy="50" fill="transparent" r="40" stroke="currentColor" stroke-width="8"></circle>
                  <circle 
                    :class="analysis.match_score >= 80 ? 'text-emerald-500' : analysis.match_score >= 60 ? 'text-amber-500' : 'text-error'"
                    class="transition-all duration-1000 ease-out" 
                    cx="50" 
                    cy="50" 
                    fill="transparent" 
                    r="40" 
                    stroke="currentColor" 
                    stroke-dasharray="251.2" 
                    :stroke-dashoffset="dashOffset" 
                    stroke-linecap="round" 
                    stroke-width="8">
                  </circle>
                </svg>
                <div class="absolute flex flex-col items-center">
                  <span class="text-4xl font-bold text-on-surface leading-none">{{ Math.round(analysis.match_score) }}%</span>
                </div>
              </div>
              <div class="flex-1 text-center md:text-left">
                <div class="inline-flex items-center px-4 py-1 rounded-full font-label-md text-label-md mb-2"
                     :class="analysis.match_score >= 80 ? 'bg-emerald-100 text-emerald-700' : analysis.match_score >= 60 ? 'bg-amber-100 text-amber-700' : 'bg-error-container text-error'">
                  <span class="material-symbols-outlined text-[16px] mr-1" style="font-variation-settings: 'FILL' 1;">
                    {{ analysis.match_score >= 80 ? 'verified' : analysis.match_score >= 60 ? 'info' : 'warning' }}
                  </span>
                  {{ analysis.match_score >= 80 ? 'Good Match' : analysis.match_score >= 60 ? 'Average Match' : 'Needs Work' }}
                </div>
                <h2 class="text-2xl font-bold text-on-surface mb-1">Job Alignment Analysis</h2>
                <p class="text-on-surface-variant text-sm">Review the missing keywords and suggestions to improve your resume score.</p>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4 mt-8 pt-8 border-t border-outline-variant/20">
              <div class="text-center border-r border-outline-variant/20">
                <p class="text-rose-600 text-lg font-bold">{{ analysis.missing_keywords?.length || 0 }}</p>
                <p class="text-on-surface-variant text-xs font-bold uppercase tracking-wider">Missing Keywords</p>
              </div>
              <div class="text-center">
                <p class="text-primary text-lg font-bold">{{ analysis.suggestions?.length || 0 }}</p>
                <p class="text-on-surface-variant text-xs font-bold uppercase tracking-wider">Suggestions</p>
              </div>
            </div>
          </Card>
          
          <!-- Keywords Card -->
          <Card class="bg-white border-outline-variant/30 rounded-xl p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)] animate-fade-in border-0 ring-1 ring-outline-variant/30" style="animation-delay: 0.2s;">
            <div>
              <h3 class="text-lg font-bold text-on-surface mb-4">Keyword Gap Analysis</h3>
              <div class="flex flex-col gap-8">
                
                <div v-if="analysis.missing_keywords?.length">
                  <p class="text-sm font-bold text-on-surface-variant mb-2 flex items-center">
                    <span class="text-rose-500 mr-2 font-bold">Missing</span> ({{ analysis.missing_keywords.length }})
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <span v-for="kw in analysis.missing_keywords" :key="kw" class="px-3 py-1 bg-rose-50 text-rose-700 border border-rose-200 rounded-lg text-xs font-medium">{{ kw }}</span>
                  </div>
                </div>
                <div v-else>
                  <p class="text-sm text-on-surface-variant">No missing keywords found! Great job.</p>
                </div>
                
              </div>
            </div>
          </Card>
          
          <!-- Bottom CTA -->
          <div class="flex justify-center mt-4">
            <NuxtLink to="/analyze">
              <Button variant="ghost" class="flex items-center gap-2 text-on-surface-variant hover:text-primary border border-transparent hover:border-primary/20 hover:bg-primary-fixed/30 px-8 py-6 rounded-lg transition-all font-bold text-sm group h-auto">
                <span class="material-symbols-outlined text-[20px] group-hover:rotate-180 transition-transform duration-500">refresh</span>
                Analyze Another Resume
              </Button>
            </NuxtLink>
          </div>
          
        </div>
        
        <!-- Right Column (40%) -->
        <div class="lg:col-span-5">
          <Card class="bg-white border-outline-variant/30 rounded-xl overflow-hidden shadow-[0_1px_3px_rgba(0,0,0,0.08)] sticky top-24 animate-fade-in border-0 ring-1 ring-outline-variant/30" style="animation-delay: 0.3s;">
            
            <!-- Tabs Header -->
            <div class="flex border-b border-outline-variant/20 bg-surface-container-low px-4 pt-4 overflow-x-auto">
              <button 
                v-for="tab in tabs" :key="tab.id"
                class="px-4 py-3 text-sm font-bold border-b-2 transition-all whitespace-nowrap"
                :class="activeTab === tab.id ? 'border-primary text-primary' : 'border-transparent text-on-surface-variant hover:text-primary'"
                @click="activeTab = tab.id"
              >
                {{ tab.label }}
              </button>
            </div>
            
            <!-- Tab Content -->
            <div class="p-6 min-h-[400px]">
              
              <!-- Summary Tab -->
              <div v-show="activeTab === 'summary'">
                <h4 class="text-lg font-bold text-on-surface mb-4">Executive Summary</h4>
                <p class="text-on-surface-variant text-base leading-relaxed mb-4">
                  Based on the AI analysis, your resume has a {{ Math.round(analysis.match_score) }}% match score for this role.
                </p>
                <p class="text-on-surface-variant text-base leading-relaxed" v-if="analysis.missing_keywords?.length">
                  The primary gap lies in missing some key technical terms required by the job description, such as {{ analysis.missing_keywords.slice(0, 2).join(' and ') }}.
                </p>
                
                <div class="mt-8 p-4 bg-primary-fixed/10 border border-primary-fixed/30 rounded-lg" v-if="analysis.suggestions?.length">
                  <p class="text-primary font-bold text-sm flex items-center mb-1">
                    <span class="material-symbols-outlined text-[18px] mr-2">lightbulb</span>
                    AI Insight
                  </p>
                  <p class="text-on-surface-variant text-sm">
                    {{ analysis.suggestions[0] }}
                  </p>
                </div>
              </div>
              
              <!-- Suggestions Tab -->
              <div v-show="activeTab === 'suggestions'">
                <h4 class="text-lg font-bold text-on-surface mb-4">Recommended Changes</h4>
                <div class="space-y-4" v-if="analysis.suggestions?.length">
                  <div class="flex gap-4" v-for="(suggestion, idx) in analysis.suggestions" :key="idx">
                    <div class="w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center flex-shrink-0 font-bold text-xs">{{ idx + 1 }}</div>
                    <p class="text-on-surface-variant text-base">{{ suggestion }}</p>
                  </div>
                </div>
                <p v-else class="text-sm text-on-surface-variant">No suggestions available.</p>
              </div>

              <!-- Hide other tabs if data is empty -->
              <div v-show="activeTab === 'strengths' || activeTab === 'weaknesses'" class="text-center py-12">
                <p class="text-sm text-on-surface-variant">This detail is not available in the current AI model output.</p>
              </div>
              
            </div>
          </Card>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card } from '~/components/ui/card/index'
import { Button } from '~/components/ui/button/index'
import { useAnalysis } from '~/composables/useAnalysis'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const router = useRouter()
const { fetchAnalysis } = useAnalysis()

const tabs = [
  { id: 'summary', label: 'Summary' },
  { id: 'strengths', label: 'Strengths' },
  { id: 'weaknesses', label: 'Weaknesses' },
  { id: 'suggestions', label: 'Suggestions' }
]

const activeTab = ref('summary')
const analysis = ref<any>(null)
const isLoading = ref(true)

// Progress ring animation
const dashOffset = ref(251.2) // Start empty (2 * PI * r = 251.2 for r=40)

onMounted(async () => {
  const id = route.query.id as string
  if (!id) {
    router.push('/dashboard')
    return
  }
  
  const result = await fetchAnalysis(id)
  if (result.success && result.data) {
    analysis.value = result.data
    // Animate to score
    setTimeout(() => {
      dashOffset.value = 251.2 - ((analysis.value.match_score / 100) * 251.2)
    }, 300)
  } else {
    alert('Failed to load analysis')
    router.push('/dashboard')
  }
  isLoading.value = false
})
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
}
</style>
