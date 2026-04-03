<script setup>
import { ref, computed, onMounted } from 'vue'
import { Check, ChevronLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import allPets from '../data/pets_data.json'

const router = useRouter()
const STORAGE_RESULTS_KEY = 'pet_recommend_results'
const STORAGE_ANSWERS_KEY = 'pet_recommend_answers'

const questions = [
    {
        key: 'type',
        category: 'Loại thú cưng',
        subtitle: 'Chọn giữa chó hoặc mèo',
        text: 'Bạn muốn nuôi gì?',
        options: [
            { text: 'Chó', value: 'dog' },
            { text: 'Mèo', value: 'cat' }
        ]
    },
    {
        key: 'energy',
        category: 'Mức năng lượng',
        subtitle: 'Ảnh hưởng đến việc vận động mỗi ngày',
        text: 'Bạn thích thú cưng vận động mức nào?',
        options: [
            { text: 'Ít vận động', value: 1 },
            { text: 'Trung bình', value: 3 },
            { text: 'Rất năng động', value: 5 }
        ]
    },
    {
        key: 'space',
        category: 'Không gian sống',
        subtitle: 'Phù hợp với diện tích nhà',
        text: 'Không gian sống của bạn?',
        options: [
            { text: 'Nhỏ', value: 1 },
            { text: 'Vừa', value: 3 },
            { text: 'Rộng', value: 5 }
        ]
    },
    {
        key: 'grooming',
        category: 'Chăm sóc',
        subtitle: 'Thời gian bạn dành để chăm thú cưng',
        text: 'Bạn có thể chăm sóc lông mức nào?',
        options: [
            { text: 'Ít chăm', value: 1 },
            { text: 'Bình thường', value: 3 },
            { text: 'Chăm kỹ', value: 5 }
        ]
    },
    {
        key: 'kid_friendly',
        category: 'Gia đình',
        subtitle: 'Mức độ thân thiện với trẻ nhỏ',
        text: 'Nhà bạn có trẻ nhỏ không?',
        options: [
            { text: 'Có, cần rất hiền', value: 1 },
            { text: 'Không quan trọng', value: 3 },
            { text: 'Không có trẻ', value: 5 }
        ]
    },
    {
        key: 'size',
        category: 'Kích thước',
        subtitle: 'Chọn kích thước thú cưng mong muốn',
        text: 'Bạn thích kích thước nào?',
        options: [
            { text: 'Nhỏ', value: 'small' },
            { text: 'Trung bình', value: 'medium' },
            { text: 'Lớn', value: 'large' }
        ]
    }
]

const currentStep = ref(0)
const answers = ref({})
const isFinished = ref(false)
const suggestedPet = ref([])

const WEIGHTS = {
    energy: 2.0,
    space: 1.5,
    grooming: 1.0,
    kid_friendly: 1.5
}

const progress = computed(() => ((currentStep.value + 1) / questions.length) * 100)

const hasCurrentAnswer = computed(() => {
    const key = questions[currentStep.value].key
    return answers.value[key] !== undefined
})

const selectedAnswersSummary = computed(() => {
    return questions.map((q) => {
        const selectedValue = answers.value[q.key]
        const selectedOption = q.options.find((opt) => opt.value === selectedValue)
        return {
            key: q.key,
            category: q.category,
            question: q.text,
            answer: selectedOption?.text || 'Chưa chọn'
        }
    })
})

const getVector = (obj) => [
    obj.energy,
    obj.space,
    obj.grooming,
    obj.kid_friendly
]

const weightedDistance = (a, b) => {
    const keys = ['energy', 'space', 'grooming', 'kid_friendly']

    return Math.sqrt(
        keys.reduce((sum, key, i) => {
            const w = WEIGHTS[key] || 1
            return sum + w * Math.pow(a[i] - b[i], 2)
        }, 0)
    )
}

const persistAnswers = () => {
    localStorage.setItem(STORAGE_ANSWERS_KEY, JSON.stringify(answers.value))
}

const getFirstUnansweredStep = () => {
    const idx = questions.findIndex((q) => answers.value[q.key] === undefined)
    return idx === -1 ? questions.length - 1 : idx
}

const selectOption = (val) => {
    const key = questions[currentStep.value].key
    answers.value[key] = val
    persistAnswers()
}

const nextStep = () => {
    const key = questions[currentStep.value].key

    if (answers.value[key] !== undefined) {
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

const calculateResult = () => {
    const filteredPets = allPets
        .filter((p) => p.id !== 'unknown')
        .filter((p) => p.type.toLowerCase() === answers.value.type)

    const userVec = getVector(answers.value)
    const results = []

    filteredPets.forEach((pet) => {
        if (answers.value.space === 1 && pet.scores.space >= 4) return
        if (answers.value.kid_friendly === 1 && pet.scores.kid_friendly >= 4) return

        const petVec = getVector(pet.scores)
        let distance = weightedDistance(userVec, petVec)

        if (pet.size !== answers.value.size) {
            distance += 1.5
        }

        const score = 100 / (1 + distance)

        results.push({
            pet,
            score,
            distance
        })
    })

    if (results.length === 0) {
        suggestedPet.value = []
        localStorage.removeItem(STORAGE_RESULTS_KEY)
        return
    }

    results.sort((a, b) => b.score - a.score)

    suggestedPet.value = results.slice(0, 3).map((item) => {
        const pet = item.pet
        const user = answers.value
        const reasons = []

        if (Math.abs(pet.scores.energy - user.energy) <= 1) {
            reasons.push('Mức năng lượng phù hợp với bạn')
        }

        if (Math.abs(pet.scores.space - user.space) <= 1) {
            reasons.push('Phù hợp với không gian sống')
        }

        if (Math.abs(pet.scores.grooming - user.grooming) <= 1) {
            reasons.push('Dễ chăm sóc theo nhu cầu của bạn')
        }

        if (Math.abs(pet.scores.kid_friendly - user.kid_friendly) <= 1) {
            reasons.push('Thân thiện với gia đình/trẻ nhỏ')
        }

        if (pet.size === user.size) {
            reasons.push('Kích thước đúng mong muốn')
        }

        return {
            name: pet.name,
            match: Math.round(item.score) + '%',
            image: pet.image_path,
            id: pet.id,
            desc: reasons.slice(0, 2).join(' • '),
            matchTags: [
                Math.abs(pet.scores.energy - user.energy) <= 1 ? 'Năng lượng' : null,
                Math.abs(pet.scores.space - user.space) <= 1 ? 'Không gian' : null,
                Math.abs(pet.scores.grooming - user.grooming) <= 1 ? 'Chăm sóc' : null,
                Math.abs(pet.scores.kid_friendly - user.kid_friendly) <= 1 ? 'Thân thiện với trẻ' : null,
                pet.size === user.size ? 'Kích thước' : null
            ].filter(Boolean)
        }
    })

    localStorage.setItem(STORAGE_RESULTS_KEY, JSON.stringify(suggestedPet.value))
}

const finishQuiz = () => {
    calculateResult()
    isFinished.value = true
}

const editAnswers = () => {
    isFinished.value = false
    currentStep.value = 0
    suggestedPet.value = []
    localStorage.removeItem(STORAGE_RESULTS_KEY)
}

const restart = () => {
    currentStep.value = 0
    answers.value = {}
    isFinished.value = false
    suggestedPet.value = []
    localStorage.removeItem(STORAGE_RESULTS_KEY)
    localStorage.removeItem(STORAGE_ANSWERS_KEY)
}

onMounted(() => {
    const savedAnswers = localStorage.getItem(STORAGE_ANSWERS_KEY)
    if (savedAnswers) {
        try {
            answers.value = JSON.parse(savedAnswers)
        } catch {
            localStorage.removeItem(STORAGE_ANSWERS_KEY)
        }
    }

    const savedResults = localStorage.getItem(STORAGE_RESULTS_KEY)
    if (savedResults) {
        try {
            suggestedPet.value = JSON.parse(savedResults)
            isFinished.value = true
        } catch {
            localStorage.removeItem(STORAGE_RESULTS_KEY)
            currentStep.value = getFirstUnansweredStep()
        }
    } else {
        currentStep.value = getFirstUnansweredStep()
    }
})
</script>

<template>
    <div
        class="pt-32 pb-20 px-4 min-h-screen flex flex-col items-center bg-[radial-gradient(circle_at_top,_rgba(20,184,166,0.12),_transparent_45%),radial-gradient(circle_at_bottom_right,_rgba(249,115,22,0.10),_transparent_40%)]">

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
