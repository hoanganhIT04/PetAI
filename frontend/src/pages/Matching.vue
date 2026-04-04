<script setup>
import { ref, computed, onMounted } from 'vue'
import { Check, ChevronLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import allPets from '../data/pets_data.json'
import {
    QUESTIONS as questions,
    MATCHING_WEIGHTS as WEIGHTS,
    STORAGE_ANSWERS_KEY,
    STORAGE_RESULTS_KEY
} from '../constants/quizData'

const router = useRouter()

// --- State ---
const currentStep = ref(0)
const answers = ref({})
const isFinished = ref(false)
const suggestedPet = ref([])

// --- Computed ---
const progress = computed(() => ((currentStep.value + 1) / questions.length) * 100)

const hasCurrentAnswer = computed(() => {
    const key = questions[currentStep.value].key
    return answers.value[key] !== undefined
})

const selectedAnswersSummary = computed(() => {
    return questions.map((q) => {
        const selectedValue = answers.value[q.key]
        // Vì selectedValue giờ là array (vd: [1,2]), ta dùng JSON.stringify để so sánh mảng
        const selectedOption = q.options.find(
            (opt) => JSON.stringify(opt.value) === JSON.stringify(selectedValue)
        )
        return {
            key: q.key,
            category: q.category,
            question: q.text,
            answer: selectedOption?.text || 'Chưa chọn'
        }
    })
})

// --- Logic Helpers ---

// Hàm phụ trợ: Kiểm tra xem điểm của Pet có nằm trong hoặc sát viền Range của User không (sai số <= 1)
const isMatchClose = (petVal, userRange) => {
    if (!userRange || !Array.isArray(userRange)) return false
    const min = userRange[0]
    const max = userRange[userRange.length - 1]
    return petVal >= min - 1 && petVal <= max + 1
}

// 1. HÀM TÍNH KHOẢNG CÁCH EUCLID MỚI (FUZZY MATCHING)
const calculateWeightedDistance = (userSelection, petScores) => {
    const keys = ['energy', 'space', 'grooming', 'kid_friendly']
    const distanceSq = keys.reduce((sum, key) => {
        const weight = WEIGHTS[key] || 1

        // userRange là 1 mảng (VD: [1, 2]). Nếu chưa có thì coi như mức trung bình [3]
        const userRange = userSelection[key] || [3]
        const petVal = petScores[key] || 3

        let diff = 0
        // Tính khoảng cách đến biên gần nhất
        if (petVal < userRange[0]) {
            diff = userRange[0] - petVal
        } else if (petVal > userRange[userRange.length - 1]) {
            diff = petVal - userRange[userRange.length - 1]
        }
        // Nếu petVal nằm trong khoảng userRange thì diff = 0 (Match 100%)

        return sum + weight * Math.pow(diff, 2)
    }, 0)
    return Math.sqrt(distanceSq)
}

// 2. HÀM TRÍCH XUẤT LÝ DO (Cập nhật đọc mảng)
const generateMatchReasons = (pet, user) => {
    const reasons = []
    if (isMatchClose(pet.scores.energy, user.energy)) reasons.push('Mức năng lượng phù hợp')
    if (isMatchClose(pet.scores.space, user.space)) reasons.push('Phù hợp không gian sống')
    if (isMatchClose(pet.scores.kid_friendly, user.kid_friendly)) reasons.push('Thân thiện gia đình')
    if (pet.size === user.size) reasons.push('Kích thước mong muốn')
    return reasons.slice(0, 2).join(' • ')
}

// --- Main Actions ---
const selectOption = (val) => {
    const key = questions[currentStep.value].key
    answers.value[key] = val
    localStorage.setItem(STORAGE_ANSWERS_KEY, JSON.stringify(answers.value))
}

const nextStep = () => {
    if (currentStep.value < questions.length - 1) {
        currentStep.value++
    } else {
        finishQuiz()
    }
}

const prevStep = () => {
    if (currentStep.value > 0) currentStep.value--
}

const calculateResult = () => {
    const user = answers.value

    const results = allPets
        .filter(p => p.id !== 'unknown' && p.type.toLowerCase() === user.type)
        .filter(pet => {
            // [HARD FILTER] - Cập nhật kiểm tra mảng
            // 1. Nhà hẹp (chọn mảng [1, 2]), loại bỏ pet cần space >= 4
            if (user.space && user.space[0] === 1 && pet.scores.space >= 4) return false

            // 2. Nhà có trẻ em (chọn mảng [4, 5]), loại bỏ pet có kid_friendly <= 2
            if (user.kid_friendly && user.kid_friendly[0] === 4 && pet.scores.kid_friendly <= 2) return false

            return true
        })
        .map(pet => {
            // Dùng trực tiếp Object truyền vào thay vì Vector tĩnh
            let distance = calculateWeightedDistance(user, pet.scores)

            // Penalty (Phạt điểm) nếu kích thước không khớp
            if (pet.size !== user.size) distance += 1.5

            // Chuẩn hóa điểm
            const score = Math.max(0, Math.min(100, 100 / (1 + distance * 0.2)))

            return {
                name: pet.name,
                id: pet.id,
                image: pet.image_path,
                match: Math.round(score) + '%',
                score,
                desc: generateMatchReasons(pet, user),
                matchTags: [
                    isMatchClose(pet.scores.energy, user.energy) ? 'Năng lượng' : null,
                    isMatchClose(pet.scores.space, user.space) ? 'Không gian' : null,
                    isMatchClose(pet.scores.kid_friendly, user.kid_friendly) ? 'Thân thiện' : null,
                    pet.size === user.size ? 'Kích thước' : null
                ].filter(Boolean)
            }
        })
        .sort((a, b) => b.score - a.score)
        .slice(0, 3)

    suggestedPet.value = results
    localStorage.setItem(STORAGE_RESULTS_KEY, JSON.stringify(results))
}

const finishQuiz = () => {
    calculateResult()
    isFinished.value = true
}

const restart = () => {
    currentStep.value = 0
    answers.value = {}
    isFinished.value = false
    suggestedPet.value = []
    localStorage.removeItem(STORAGE_RESULTS_KEY)
    localStorage.removeItem(STORAGE_ANSWERS_KEY)
}

const editAnswers = () => {
    isFinished.value = false
    currentStep.value = 0
}

onMounted(() => {
    const savedAnswers = localStorage.getItem(STORAGE_ANSWERS_KEY)
    const savedResults = localStorage.getItem(STORAGE_RESULTS_KEY)

    if (savedAnswers) answers.value = JSON.parse(savedAnswers)

    if (savedResults) {
        suggestedPet.value = JSON.parse(savedResults)
        isFinished.value = true
    } else {
        const unansweredIdx = questions.findIndex(q => answers.value[q.key] === undefined)
        currentStep.value = unansweredIdx === -1 ? 0 : unansweredIdx
    }
})
</script>

<template>
    <div
        class="pt-32 pb-20 px-4 min-h-screen flex flex-col items-center
      bg-[radial-gradient(circle_at_top,_rgba(20,184,166,0.12),_transparent_45%),radial-gradient(circle_at_bottom_right,_rgba(249,115,22,0.10),_transparent_40%)]">

        <div v-if="!isFinished" class="max-w-2xl w-full mb-8">
            <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-bold text-teal-600 uppercase tracking-widest">Tiến trình: {{
                    Math.round(progress) }}%</span>
                <span class="text-xs text-slate-400 font-medium">Câu hỏi {{ currentStep + 1 }} / {{ questions.length
                }}</span>
            </div>
            <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                <div class="bg-teal-500 h-full transition-all duration-500 ease-out" :style="{ width: `${progress}%` }">
                </div>
            </div>
        </div>

        <div v-if="!isFinished"
            class="max-w-2xl w-full bg-white/90 backdrop-blur rounded-[2rem] shadow-xl shadow-slate-200/50 overflow-hidden p-6 md:p-10 border border-slate-100 relative">
            <transition name="slide-fade" mode="out-in">
                <div :key="currentStep">
                    <div class="text-center mb-10">
                        <div
                            class="inline-block bg-orange-100 text-orange-600 px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter mb-4">
                            {{ questions[currentStep].category }}
                        </div>
                        <h2 class="text-2xl md:text-3xl font-black text-slate-900 leading-tight">{{
                            questions[currentStep].text }}</h2>
                        <p class="text-slate-500 mt-4">{{ questions[currentStep].subtitle }}</p>
                    </div>

                    <div class="grid grid-cols-1 gap-4">
                        <button v-for="opt in questions[currentStep].options" :key="opt.value"
                            @click="selectOption(opt.value)"
                            class="group flex items-center justify-between p-4 border-2 rounded-2xl transition-all duration-300 text-left active:scale-[0.98]"
                            :class="answers[questions[currentStep].key] === opt.value ? 'border-teal-500 bg-teal-50 shadow-md shadow-teal-100/60' : 'border-slate-100 hover:border-teal-400 hover:bg-teal-50/30'">
                            <div>
                                <p class="font-bold text-base text-slate-800"
                                    :class="answers[questions[currentStep].key] === opt.value ? 'text-teal-800' : ''">{{
                                        opt.text }}
                                </p>
                            </div>
                            <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center transition-all"
                                :class="answers[questions[currentStep].key] === opt.value ? 'border-teal-500 bg-teal-500' : 'border-slate-200 group-hover:border-teal-400'">
                                <Check v-if="answers[questions[currentStep].key] === opt.value"
                                    class="text-white w-5 h-5" />
                            </div>
                        </button>
                    </div>

                    <div class="mt-12 flex justify-between items-center">
                        <button @click="prevStep"
                            class="text-slate-400 font-bold hover:text-slate-900 transition flex items-center gap-2 group disabled:opacity-0"
                            :disabled="currentStep === 0">
                            <ChevronLeft class="w-5 h-5 transition group-hover:-translate-x-1" /> Quay lại
                        </button>
                        <button @click="nextStep" :disabled="!hasCurrentAnswer"
                            class="bg-orange-500 text-white px-10 py-4 rounded-2xl font-black shadow-lg shadow-orange-500/30 hover:bg-orange-600 hover:-translate-y-1 transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                            {{ currentStep === questions.length - 1 ? 'HOÀN TẤT' : 'TIẾP THEO' }}
                        </button>
                    </div>
                </div>
            </transition>
        </div>

        <div v-else class="max-w-5xl w-full">
            <div
                class="text-center mb-8 bg-white/85 backdrop-blur rounded-3xl border border-slate-100 shadow-lg p-6 md:p-8">
                <h2 class="text-3xl font-extrabold text-slate-900 mb-2">Kết quả phân tích</h2>
                <p class="text-slate-500">Top 3 thú cưng phù hợp với bạn</p>
            </div>

            <div class="bg-white rounded-3xl border border-slate-100 shadow-lg p-5 md:p-7 mb-8">
                <div class="flex items-center justify-between flex-wrap gap-3 mb-4">
                    <h3 class="text-xl font-extrabold text-slate-900">Bạn đã chọn</h3>
                    <button @click="editAnswers"
                        class="text-sm font-bold px-4 py-2 rounded-xl bg-teal-50 text-teal-700 hover:bg-teal-100 transition">
                        Sửa câu trả lời
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div v-for="item in selectedAnswersSummary" :key="item.key"
                        class="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                        <div class="text-[11px] uppercase tracking-wider font-black text-slate-500 mb-1">
                            {{ item.category }}
                        </div>
                        <p class="text-sm text-slate-600 mb-1">{{ item.question }}</p>
                        <p class="font-bold text-slate-900">{{ item.answer }}</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div v-for="(pet, index) in suggestedPet" :key="pet.id"
                    class="bg-white rounded-3xl p-6 shadow-xl border border-slate-100 relative hover:-translate-y-1 transition">
                    <div v-if="index === 0"
                        class="absolute -top-3 left-1/2 -translate-x-1/2 bg-orange-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                        Lựa chọn tốt nhất
                    </div>

                    <div class="text-sm text-teal-600 font-bold mb-2">
                        Xác suất: {{ pet.match }}
                    </div>

                    <div class="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4 ring-4 ring-slate-50">
                        <img :src="pet.image" class="w-full h-full object-cover" :alt="pet.name">
                    </div>

                    <h3 class="text-xl font-bold mb-2 min-h-[56px] leading-tight">
                        {{ pet.name }}
                    </h3>

                    <p class="text-sm text-slate-500 mb-4 min-h-[40px]">
                        {{ pet.desc }}
                    </p>

                    <div class="mb-4 flex flex-wrap gap-2 min-h-[56px] content-start">
                        <span v-for="tag in pet.matchTags" :key="tag"
                            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            {{ tag }}
                        </span>
                    </div>

                    <button @click="router.push({
                        path: `/info/${pet.id}`,
                        query: { from: 'matching' }
                    })"
                        class="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-teal-700 transition">
                        Xem chi tiết
                    </button>
                </div>
            </div>

            <button @click="restart"
                class="mt-8 bg-white text-slate-500 border px-6 py-3 rounded-xl font-bold hover:bg-slate-50">
                Làm lại
            </button>
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