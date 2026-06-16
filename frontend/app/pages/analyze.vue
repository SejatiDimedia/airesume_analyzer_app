<template>
  <div class="flex justify-center pt-8">
    <Card class="bg-white w-full max-w-[720px] rounded-xl border-outline-variant/20 shadow-[0_1px_3px_rgba(0,0,0,0.08)] overflow-hidden relative border-0 ring-1 ring-outline-variant/20">
      
      <!-- Analysis Form Content -->
      <div class="p-8 space-y-8" :class="{ 'opacity-0 pointer-events-none': isAnalyzing }">
        <div class="flex flex-col gap-1">
          <h1 class="font-headline-lg text-headline-lg text-on-surface tracking-tight">New Analysis</h1>
          <p class="text-on-surface-variant font-body-md text-body-md">Optimize your resume against specific job requirements with AI.</p>
        </div>

        <div v-if="errorMessage" class="bg-error/10 border border-error/20 text-error px-4 py-3 rounded-lg text-body-md">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">error</span>
            <p>{{ errorMessage }}</p>
          </div>
        </div>
        
        <!-- Section 1: Your Resume -->
        <section class="space-y-4">
          <div class="flex justify-between items-center">
            <h2 class="font-headline-sm text-headline-sm text-on-surface">Your Resume</h2>
            <div v-if="hasSavedProfile" class="flex gap-2 bg-surface-container-low p-1 rounded-lg border border-outline-variant/30">
              <button 
                @click="useSavedProfile = true" 
                :class="useSavedProfile ? 'bg-primary text-white' : 'text-on-surface-variant hover:bg-surface-variant/30'"
                class="px-3 py-1 rounded-md text-label-sm font-label-sm transition-all"
              >
                Use Saved Profile
              </button>
              <button 
                @click="useSavedProfile = false" 
                :class="!useSavedProfile ? 'bg-primary text-white' : 'text-on-surface-variant hover:bg-surface-variant/30'"
                class="px-3 py-1 rounded-md text-label-sm font-label-sm transition-all"
              >
                Upload New
              </button>
            </div>
          </div>
          
          <div v-if="hasSavedProfile && useSavedProfile" class="p-6 bg-green-50 border border-green-200 rounded-xl flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600">
                <span class="material-symbols-outlined">description</span>
              </div>
              <div>
                <p class="font-body-md text-body-md text-green-800 font-bold">Using Saved Base Resume</p>
                <p class="font-body-sm text-body-sm text-green-700">Your profile will be used for this analysis.</p>
              </div>
            </div>
            <NuxtLink to="/profile" class="text-green-600 hover:text-green-800 underline font-label-sm text-label-sm">
              Manage Profile
            </NuxtLink>
          </div>

          <div v-else class="dashed-border group cursor-pointer hover:bg-surface-container-low transition-colors duration-200" @click="triggerFileInput">
            <div class="flex flex-col items-center justify-center py-12 px-6 text-center">
              <span class="material-symbols-outlined text-primary text-[48px] mb-4">cloud_upload</span>
              <p class="font-body-md text-body-md text-on-surface font-semibold" v-if="!selectedFile">Drag & drop your resume here</p>
              <p class="font-body-md text-body-md text-primary font-semibold" v-else>{{ selectedFile.name }}</p>
              <p class="font-body-sm text-body-sm text-on-surface-variant mt-1" v-if="!selectedFile">Support PDF, DOCX (Max 10MB)</p>
              <Button variant="link" class="mt-4 text-primary font-label-md text-label-md" @click.stop="triggerFileInput">
                {{ selectedFile ? 'Change file' : 'or browse files' }}
              </Button>
              <input type="file" ref="fileInput" class="hidden" accept=".pdf,.docx" @change="onFileChange" />
            </div>
          </div>
        </section>
        
        <!-- Section 2: Job Description -->
        <section class="space-y-4">
          <div class="flex justify-between items-center flex-wrap gap-2">
            <h2 class="font-headline-sm text-headline-sm text-on-surface">Job Description</h2>
            <div class="flex items-center gap-3">
              <button 
                @click="showUrlInput = !showUrlInput" 
                class="text-primary hover:text-primary-hover transition-colors font-label-md text-label-md flex items-center gap-1 hover:underline bg-primary/5 px-3 py-1 rounded-lg"
              >
                <span class="material-symbols-outlined text-[16px]">{{ showUrlInput ? 'close' : 'link' }}</span>
                {{ showUrlInput ? 'Cancel Import' : 'Import from URL' }}
              </button>
              <div class="flex items-center gap-1 bg-tertiary-fixed/30 px-2 py-1 rounded-full">
                <span class="material-symbols-outlined text-on-tertiary-fixed-variant text-[16px]">info</span>
                <span class="text-on-tertiary-fixed-variant font-label-sm text-label-sm">Include requirements</span>
              </div>
            </div>
          </div>

          <!-- URL Import Input Panel -->
          <div v-if="showUrlInput" class="p-4 bg-surface-container rounded-xl border border-outline-variant/30 space-y-3 animate-fade-in">
            <p class="text-xs text-on-surface-variant font-body-sm">Masukkan URL lowongan kerja (LinkedIn, Jobstreet, dsb) untuk mengekstrak detail lowongan menggunakan AI.</p>
            <div class="flex gap-2">
              <Input 
                v-model="jdUrl"
                placeholder="https://example.com/job-vacancy" 
                class="flex-1 rounded-lg border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary/20 font-body-sm text-body-sm px-4 py-2 h-10 bg-white"
                :disabled="isFetchingUrl"
                @keyup.enter="fetchJobDescription"
              />
              <Button 
                @click="fetchJobDescription" 
                :disabled="isFetchingUrl || !jdUrl.trim()"
                class="bg-primary !text-white px-5 rounded-lg h-10 font-label-md text-label-md flex items-center gap-1.5"
              >
                <span class="material-symbols-outlined text-[18px] animate-spin" v-if="isFetchingUrl">sync</span>
                <span class="material-symbols-outlined text-[18px]" v-else>cloud_download</span>
                {{ isFetchingUrl ? 'Fetching...' : 'Import' }}
              </Button>
            </div>
            <p v-if="urlErrorMessage" class="text-xs text-error flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px]">error</span>
              {{ urlErrorMessage }}
            </p>
            <p v-if="urlSuccessMessage" class="text-xs text-emerald-600 flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px]">check_circle</span>
              {{ urlSuccessMessage }}
            </p>
          </div>

          <div class="relative">
            <Textarea 
              v-model="jobDescription"
              class="w-full rounded-lg border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all font-body-md text-body-md p-6 resize-none min-h-[150px]" 
              placeholder="Paste the job description or specific requirements here..." 
            />
          </div>
        </section>
        
        <!-- Section 3: Label -->
        <section class="space-y-2">
          <Label for="analysis-label" class="font-headline-sm text-headline-sm text-on-surface block">
            Label <span class="text-on-surface-variant font-body-sm font-normal">(optional)</span>
          </Label>
          <Input 
            v-model="analysisLabel"
            id="analysis-label" 
            placeholder="e.g., Senior Product Designer - Google" 
            class="w-full rounded-lg border-outline-variant focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all font-body-md text-body-md px-6 py-4 h-auto" 
          />
        </section>
        
        <!-- Actions -->
        <div class="pt-8 flex items-center justify-end gap-4">
          <NuxtLink to="/dashboard">
            <Button variant="ghost" class="text-on-surface-variant hover:bg-surface-variant/30 px-8 py-6 rounded-lg font-label-md text-label-md transition-all active:scale-95 h-auto">
              Cancel
            </Button>
          </NuxtLink>
          <Button 
            class="bg-primary !text-white px-12 py-6 rounded-lg font-label-md text-label-md shadow-md hover:-translate-y-0.5 hover:shadow-lg transition-all active:scale-95 flex items-center gap-2 h-auto" 
            @click="startAnalysis"
            :disabled="!isValid"
          >
            Analyze Resume 
            <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
          </Button>
        </div>
      </div>
      
      <!-- Loading Overlay -->
      <div 
        class="absolute inset-0 glass-overlay z-10 flex flex-col items-center justify-center p-12 text-center space-y-6 transition-opacity duration-500" 
        :class="isAnalyzing ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'"
      >
        <div class="relative w-24 h-24">
          <!-- Progress Ring -->
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 96 96">
            <circle class="text-surface-variant" cx="48" cy="48" fill="transparent" r="44" stroke="currentColor" stroke-width="4"></circle>
            <circle class="text-primary animate-dash" cx="48" cy="48" fill="transparent" r="44" stroke="currentColor" stroke-linecap="round" stroke-width="4" style="stroke-dasharray: 276; stroke-dashoffset: 60;"></circle>
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="material-symbols-outlined text-primary text-[32px] animate-pulse">auto_awesome</span>
          </div>
        </div>
        
        <div class="space-y-2">
          <h3 class="font-headline-sm text-headline-sm text-on-surface">AI is analyzing your resume...</h3>
          <p class="text-on-surface-variant font-body-md text-body-md max-w-[300px] mx-auto">Extracting skills and comparing requirements to find your perfect match.</p>
        </div>
        
        <div class="w-full max-w-[240px] h-1.5 bg-surface-variant rounded-full overflow-hidden">
          <div class="h-full bg-primary animate-[loading-bar_2s_infinite_linear] w-[30%]"></div>
        </div>
      </div>
      
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Card } from '~/components/ui/card/index'
import { Button } from '~/components/ui/button/index'
import { Textarea } from '~/components/ui/textarea/index'
import { Input } from '~/components/ui/input/index'
import { Label } from '~/components/ui/label/index'
import { useAnalysis } from '~/composables/useAnalysis'
import { useProfile } from '~/composables/useProfile'
import { useAuth } from '~/composables/useAuth'
import { onMounted } from 'vue'

definePageMeta({
  middleware: 'auth'
})

const router = useRouter()
const { analyzeResume } = useAnalysis()
const { fetchSavedResume } = useProfile()
const { apiFetch } = useAuth()

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const jobDescription = ref('')
const analysisLabel = ref('')
const isAnalyzing = ref(false)
const errorMessage = ref('')

// URL Scrape state
const showUrlInput = ref(false)
const jdUrl = ref('')
const isFetchingUrl = ref(false)
const urlErrorMessage = ref('')
const urlSuccessMessage = ref('')

const fetchJobDescription = async () => {
  if (!jdUrl.value.trim()) return
  isFetchingUrl.value = true
  urlErrorMessage.value = ''
  urlSuccessMessage.value = ''
  
  try {
    const res = await apiFetch<{ job_title: string, job_description: string }>(
      '/analysis/scrape-jd',
      {
        method: 'POST',
        body: { url: jdUrl.value.trim() }
      }
    )
    if (res && res.job_description) {
      jobDescription.value = res.job_description
      if (res.job_title) {
        analysisLabel.value = res.job_title
      }
      urlSuccessMessage.value = 'Deskripsi pekerjaan berhasil diekstrak!'
      // Hide input after a short delay
      setTimeout(() => {
        showUrlInput.value = false
        urlSuccessMessage.value = ''
        jdUrl.value = ''
      }, 2000)
    } else {
      urlErrorMessage.value = 'Gagal mengekstrak deskripsi pekerjaan. Coba salin manual.'
    }
  } catch (error: any) {
    urlErrorMessage.value = error.data?.detail || 'Gagal mengambil deskripsi dari URL tersebut.'
  } finally {
    isFetchingUrl.value = false
  }
}

const hasSavedProfile = ref(false)
const useSavedProfile = ref(false)

onMounted(async () => {
  const profile = await fetchSavedResume()
  if (profile.has_profile) {
    hasSavedProfile.value = true
    useSavedProfile.value = true
  }
})

const isValid = computed(() => {
  const hasResume = useSavedProfile.value || selectedFile.value !== null
  return hasResume && jobDescription.value.trim().length > 0
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

const startAnalysis = async () => {
  if (!isValid.value) return
  
  const fileToAnalyze = useSavedProfile.value ? null : selectedFile.value
  
  isAnalyzing.value = true
  errorMessage.value = ''
  
  const result = await analyzeResume(fileToAnalyze, jobDescription.value, analysisLabel.value || undefined)
  
  if (result.success && result.data?.id) {
    // Redirect to the newly created analysis result page
    router.push(`/result?id=${result.data.id}`)
  } else {
    isAnalyzing.value = false
    errorMessage.value = result.error || 'Failed to process analysis. Please try again.'
  }
}
</script>

<style scoped>
.glass-overlay {
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.8);
}

.dashed-border {
  background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' rx='8' ry='8' stroke='%23CBC4D2FF' stroke-width='2' stroke-dasharray='8%2c 8' stroke-dashoffset='0' stroke-linecap='square'/%3e%3c/svg%3e");
  border-radius: 8px;
}

@keyframes loading-bar {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(300%); }
}

@keyframes dash {
  to { stroke-dashoffset: 0; }
}

.animate-dash {
  animation: dash 3s ease-in-out infinite alternate;
}
</style>
