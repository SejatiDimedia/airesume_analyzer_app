import { ref } from 'vue'
import { useAuth } from '~/composables/useAuth'

export function useAnalysis() {
  const { apiFetch } = useAuth()
  
  const extractText = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    // apiFetch handles auth headers automatically
    const res: any = await apiFetch('/upload/test-parse', {
      method: 'POST',
      body: formData
    })
    return res.extracted_text
  }

  const createAnalysis = async (resumeText: string, jobDescription: string, label?: string) => {
    const res: any = await apiFetch('/analysis/', {
      method: 'POST',
      body: {
        resume_text: resumeText,
        job_description: jobDescription,
        label: label
      }
    })
    return res
  }

  const analyzeResume = async (file: File, jobDescription: string, label?: string) => {
    try {
      // 1. Extract text from PDF/DOCX
      const resumeText = await extractText(file)
      
      // 2. Create analysis with the extracted text and JD
      const analysis = await createAnalysis(resumeText, jobDescription, label)
      
      return { success: true, data: analysis }
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.response?._data?.detail || error.message }
    }
  }

  const fetchHistory = async (page = 1, size = 10) => {
    try {
      const res: any = await apiFetch(`/analysis/?page=${page}&size=${size}`)
      return { success: true, data: res }
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.message }
    }
  }

  const fetchAnalysis = async (id: string) => {
    try {
      const res: any = await apiFetch(`/analysis/${id}`)
      return { success: true, data: res }
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.message }
    }
  }

  const deleteAnalysis = async (id: string) => {
    try {
      await apiFetch(`/analysis/${id}`, {
        method: 'DELETE'
      })
      return { success: true }
    } catch (error: any) {
      console.error(error)
      return { success: false, error: error.message }
    }
  }

  return {
    analyzeResume,
    fetchHistory,
    fetchAnalysis,
    deleteAnalysis
  }
}
