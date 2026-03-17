<script setup>
import { ref } from 'vue'
import { UploadCloud, Loader2, ArrowRight, RotateCw } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInput = ref(null)
const previewImage = ref(null)
const isScanning = ref(false)
const scanResult = ref(null)

const triggerUpload = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target.result
      startScan()
    }
    reader.readAsDataURL(file)
  }
}

const startScan = async () => {
  isScanning.value = true
  scanResult.value = null

  const formData = new FormData()
  formData.append("file", fileInput.value.files[0])

  try {
    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      body: formData
    })

    const data = await res.json()

    if (!data.success) {
      scanResult.value = {
        error: true,
        message: data.message,
        confidence: data.confidence + "%"
      }
      return
    }

    scanResult.value = {
      breed: data.breed,
      confidence: data.confidence + "%"
    }

  } catch (err) {
    alert("AI server error")
    console.error(err)
  } finally {
    isScanning.value = false
  }
}


const resetScan = () => {
    previewImage.value = null
    scanResult.value = null
    if (fileInput.value) {
        fileInput.value.value = '' // Reset input
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatBreed = (name) => {
  return name
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}

</script>

<template>
  <div class="pt-32 pb-20 px-4 min-h-[90vh] flex flex-col justify-center">
    <div class="max-w-4xl mx-auto text-center w-full">
      <h1 class="text-4xl font-extrabold text-slate-900 mb-4">AI Breed <span class="text-teal-600">Scanner</span></h1>
      <p class="text-lg text-slate-600 mb-8">Tải ảnh lên để nhận diện giống chó/mèo và tra cứu thông tin chi tiết.</p>

      <!-- Dropzone Area -->
      <transition name="fade" mode="out-in">
        <div 
            v-if="!previewImage"
            @click="triggerUpload" 
            class="border-4 border-dashed border-slate-200 rounded-[2rem] p-8 bg-white hover:border-teal-400 transition cursor-pointer group shadow-xl max-w-2xl mx-auto min-h-[250px] flex flex-col justify-center items-center"
        >
            <div class="flex flex-col items-center gap-6 text-slate-400 group-hover:text-teal-600">
            <UploadCloud class="w-20 h-20 transition-transform group-hover:scale-110" />
            <p class="text-2xl font-bold">Kéo thả ảnh hoặc click để chọn file</p>
            <span class="text-base bg-slate-100 px-4 py-2 rounded-lg font-medium">Hỗ trợ: JPG, PNG, WEBP</span>
            <input 
                type="file" 
                ref="fileInput" 
                class="hidden" 
                accept="image/*"
                @change="handleFileChange"
            >
            </div>
        </div>

        <!-- Scanning/Result State -->
        <div v-else class="max-w-3xl mx-auto">
            
            <!-- Loading State -->
            <div v-if="isScanning" class="border-4 border-dashed border-teal-100 rounded-[2rem] p-8 bg-teal-50 min-h-[250px] flex flex-col justify-center items-center">
                <div class="flex flex-col items-center gap-6 text-teal-600 animate-pulse">
                    <Loader2 class="w-20 h-20 animate-spin" />
                    <p class="text-2xl font-bold italic">AI đang phân tích hình ảnh...</p>
                </div>
            </div>

            <!-- Result State -->
          <div v-if="scanResult" id="result-preview" class="mt-8">

            <!--CASE: Ảnh không hợp lệ -->
            <div
              v-if="scanResult.error"
              class="bg-red-50 p-8 rounded-[2.5rem] shadow-2xl border-4 border-red-400 text-center"
            >
              <div class="flex flex-col items-center gap-6">
                <div class="w-64 h-64 bg-slate-200 rounded-3xl overflow-hidden shadow-md">
                  <img :src="previewImage" class="w-full h-full object-cover">
                </div>

                <h3 class="text-4xl font-black text-red-600">
                  Không nhận diện được
                </h3>

                <p class="text-slate-600 text-lg max-w-xl">
                  {{ scanResult.message }}
                </p>

                <p class="text-red-500 font-bold">
                  Độ tin cậy: {{ scanResult.confidence }}
                </p>

                <button
                  @click="resetScan"
                  class="mt-4 bg-white border-2 border-red-400 text-red-600 px-8 py-4 rounded-xl font-bold hover:bg-red-100 transition flex items-center gap-2"
                >
                  <RotateCw class="w-5 h-5" /> Quét ảnh khác
                </button>
              </div>
            </div>

            <!--CASE: Nhận diện thành công -->
            <div
              v-else
              class="bg-white p-8 rounded-[2.5rem] shadow-2xl border-4 border-teal-500 relative"
            >
              <div class="flex flex-col md:flex-row items-center gap-10">
                <div class="w-64 h-64 bg-slate-200 rounded-3xl overflow-hidden shadow-md shrink-0">
                  <img :src="previewImage" class="w-full h-full object-cover">
                </div>

                <div class="text-left flex-1">
                  <span class="text-teal-600 font-black text-sm uppercase tracking-[0.2em] block mb-2">
                    Kết quả phân tích
                  </span>

                  <h3
                    class="text-5xl font-black italic text-slate-900 mb-3 leading-tight max-w-[28rem] line-clamp-2"
                  >
                    {{ formatBreed(scanResult.breed) }}
                  </h3>

                  <p class="text-slate-500 font-medium text-lg mb-6 flex items-center gap-2">
                    Độ tin cậy:
                    <span class="text-teal-600 font-bold bg-teal-50 px-2 py-0.5 rounded">
                      {{ scanResult.confidence }}
                    </span>
                  </p>

                  <div class="flex flex-col gap-3">
                    <RouterLink
                      :to="`/info/${scanResult.breed}`"
                      class="w-full bg-slate-900 text-white py-4 rounded-xl font-bold hover:bg-teal-700 transition flex items-center justify-center gap-2 text-lg shadow-lg"
                    >
                      Xem thông tin chi tiết <ArrowRight class="w-5 h-5" />
                    </RouterLink>

                    <button
                      @click="resetScan"
                      class="w-full bg-white border-2 border-slate-200 text-slate-600 py-4 rounded-xl font-bold hover:border-teal-400 hover:text-teal-600 transition flex items-center justify-center gap-2 text-lg"
                    >
                      <RotateCw class="w-5 h-5" /> Quét ảnh khác
                    </button>
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>
      </transition>

    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
