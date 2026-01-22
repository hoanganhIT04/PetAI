<script setup>
import { ref, computed } from 'vue'
import { Check, ChevronLeft, ArrowRight, RotateCcw } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const questions = [
  {
    category: "Thói quen sinh hoạt",
    text: "Bạn có thường xuyên đi vắng không?",
    subtitle: "Điều này giúp chọn loài vật có khả năng tự lập.",
    options: [
      { text: "Làm việc tại nhà", sub: "Có thể dành 5-8 tiếng/ngày", value: 1 },
      { text: "Đi làm hành chính", sub: "Vắng nhà 8-10 tiếng", value: 2 },
      { text: "Hay đi công tác", sub: "Cần loài cực kỳ tự lập", value: 3 }
    ]
  },
  {
    category: "Không gian sống",
    text: "Diện tích nhà bạn thế nào?",
    subtitle: "Kích thước thú cưng cần phù hợp với không gian.",
    options: [
      { text: "Chung cư nhỏ / Phòng trọ", sub: "< 30m2", value: 1 },
      { text: "Căn hộ trung bình", sub: "30-70m2", value: 2 },
      { text: "Nhà phố / Biệt thự", sub: "Có sân vườn rộng", value: 3 }
    ]
  },
  {
    category: "Mức năng lượng",
    text: "Bạn thích vận động mức nào?",
    subtitle: "Ảnh hưởng đến việc dắt thú cưng đi dạo.",
    options: [
      { text: "Chill tại nhà", sub: "Thích nằm sofa xem phim", value: 1 },
      { text: "Đi dạo nhẹ nhàng", sub: "30p mỗi ngày", value: 2 },
      { text: "Chạy bộ / Thể thao", sub: "Vận động mạnh mỗi ngày", value: 3 }
    ]
  },
  {
    category: "Kinh nghiệm",
    text: "Bạn từng nuôi thú cưng chưa?",
    subtitle: "Một số loài cần người nuôi có kinh nghiệm.",
    options: [
      { text: "Lần đầu nuôi", sub: "Cần loài dễ tính, dễ dạy", value: 1 },
      { text: "Đã từng nuôi", sub: "Biết chăm sóc cơ bản", value: 2 },
      { text: "Chuyên gia", sub: "Hiểu rõ tâm lý thú cưng", value: 3 }
    ]
  },
  {
    category: "Ngân sách",
    text: "Khả năng chi trả hàng tháng?",
    subtitle: "Bao gồm thức ăn, spa, y tế.",
    options: [
      { text: "Tiết kiệm", sub: "< 1 triệu/tháng", value: 1 },
      { text: "Trung bình", sub: "1 - 3 triệu/tháng", value: 2 },
      { text: "Thoải mái", sub: "> 3 triệu/tháng", value: 3 }
    ]
  }
]

const currentStep = ref(0)
const answers = ref({})
const isFinished = ref(false)

const progress = computed(() => {
    return ((currentStep.value + 1) / questions.length) * 100
})

const selectOption = (val) => {
    answers.value[currentStep.value] = val
}

const nextStep = () => {
    if (answers.value[currentStep.value]) {
        if (currentStep.value < questions.length - 1) {
            currentStep.value++
        } else {
            finishQuiz()
        }
    }
}

const prevStep = () => {
    if (currentStep.value > 0) {
        currentStep.value--
    }
}

const finishQuiz = () => {
    // Fake processing
    isFinished.value = true
}

const restart = () => {
    currentStep.value = 0
    answers.value = {}
    isFinished.value = false
}

const suggestedPet = {
    name: "Golden Retriever",
    desc: "Bạn là người hướng ngoại, có không gian sống rộng và thích vận động. Golden Retriever là người bạn lý tưởng với tính cách thân thiện, trung thành và tràn đầy năng lượng.",
    match: "96%"
}
</script>

<template>
  <div class="pt-32 pb-20 px-4 min-h-screen flex flex-col items-center">
    
    <!-- Progress Header -->
    <div v-if="!isFinished" class="max-w-2xl w-full mb-8">
        <div class="flex justify-between items-center mb-2">
            <span class="text-sm font-bold text-teal-600 uppercase tracking-widest">Tiến trình: {{ Math.round(progress) }}%</span>
            <span class="text-xs text-slate-400 font-medium">Câu hỏi {{ currentStep + 1 }} / {{ questions.length }}</span>
        </div>
        <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div 
                class="bg-teal-500 h-full transition-all duration-500 ease-out"
                :style="{ width: `${progress}%` }"
            ></div>
        </div>
    </div>

    <!-- Quiz Card -->
    <div v-if="!isFinished" class="max-w-2xl w-full bg-white rounded-[3rem] shadow-xl shadow-slate-200/50 overflow-hidden p-8 md:p-14 border border-slate-100 relative">
        <transition name="slide-fade" mode="out-in">
            <div :key="currentStep">
                <div class="text-center mb-10">
                    <div class="inline-block bg-orange-100 text-orange-600 px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter mb-4">
                        {{ questions[currentStep].category }}
                    </div>
                    <h2 class="text-3xl md:text-4xl font-black text-slate-900 leading-tight">{{ questions[currentStep].text }}</h2>
                    <p class="text-slate-500 mt-4">{{ questions[currentStep].subtitle }}</p>
                </div>

                <div class="grid grid-cols-1 gap-4">
                    <button 
                        v-for="opt in questions[currentStep].options" 
                        :key="opt.value"
                        @click="selectOption(opt.value)"
                        class="group flex items-center justify-between p-6 border-2 rounded-3xl transition-all duration-300 text-left active:scale-[0.98]"
                        :class="answers[currentStep] === opt.value ? 'border-teal-500 bg-teal-50' : 'border-slate-100 hover:border-teal-400 hover:bg-teal-50/30'"
                    >
                        <div>
                            <p class="font-bold text-lg text-slate-800" :class="answers[currentStep] === opt.value ? 'text-teal-800' : ''">{{ opt.text }}</p>
                            <p class="text-sm text-slate-400">{{ opt.sub }}</p>
                        </div>
                        <div 
                            class="w-8 h-8 rounded-full border-2 flex items-center justify-center transition-all"
                            :class="answers[currentStep] === opt.value ? 'border-teal-500 bg-teal-500' : 'border-slate-200 group-hover:border-teal-400'"
                        >
                            <Check v-if="answers[currentStep] === opt.value" class="text-white w-5 h-5" />
                        </div>
                    </button>
                </div>

                <div class="mt-12 flex justify-between items-center">
                    <button 
                        @click="prevStep" 
                        class="text-slate-400 font-bold hover:text-slate-900 transition flex items-center gap-2 group disabled:opacity-0"
                        :disabled="currentStep === 0"
                    >
                        <ChevronLeft class="w-5 h-5 transition group-hover:-translate-x-1" /> Quay lại
                    </button>
                    <button 
                        @click="nextStep"
                        :disabled="!answers[currentStep]"
                        class="bg-orange-500 text-white px-10 py-4 rounded-2xl font-black shadow-lg shadow-orange-500/30 hover:bg-orange-600 hover:-translate-y-1 transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    >
                        {{ currentStep === questions.length - 1 ? 'HOÀN TẤT' : 'TIẾP THEO' }}
                    </button>
                </div>
            </div>
        </transition>
    </div>

    <!-- Result Card -->
    <div v-else class="max-w-2xl w-full text-center">
        <h2 class="text-4xl font-extrabold text-slate-900 mb-2">Kết quả phân tích</h2>
        <p class="text-slate-500 mb-8">Dựa trên 5 câu trả lời của bạn</p>
        
        <div class="bg-white rounded-[3rem] p-8 md:p-12 shadow-2xl border-4 border-teal-500 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-teal-400 to-orange-400"></div>
            
            <div class="inline-block bg-teal-100 text-teal-700 font-bold px-4 py-1 rounded-full text-sm mb-6">
                Độ phù hợp: {{ suggestedPet.match }}
            </div>

            <div class="w-48 h-48 mx-auto rounded-full overflow-hidden border-8 border-slate-100 mb-6 shadow-inner">
                <img src="https://images.unsplash.com/photo-1552053831-71594a27632d?w=400" class="w-full h-full object-cover">
            </div>
            
            <h3 class="text-3xl font-black text-slate-800 mb-4">{{ suggestedPet.name }}</h3>
            <p class="text-slate-600 mb-8 leading-relaxed">{{ suggestedPet.desc }}</p>

            <div class="flex flex-col md:flex-row gap-4 justify-center">
                <button @click="router.push('/info/1')" class="bg-slate-900 text-white px-8 py-3 rounded-xl font-bold hover:bg-teal-700 transition flex items-center justify-center gap-2">
                    Xem chi tiết <ArrowRight class="w-4 h-4"/>
                </button>
                <button @click="restart" class="bg-white text-slate-500 border border-slate-200 px-8 py-3 rounded-xl font-bold hover:bg-slate-50 transition flex items-center justify-center gap-2">
                    <RotateCcw class="w-4 h-4"/> Làm lại
                </button>
            </div>
        </div>
    </div>

  </div>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
