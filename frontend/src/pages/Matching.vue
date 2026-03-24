<script setup>
import { ref, computed, onMounted } from 'vue'
import { Check, ChevronLeft, ArrowRight, RotateCcw } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import allPets from '../data/pets_data.json'

const router = useRouter()

onMounted(() => {
    const saved = localStorage.getItem("pet_recommend_results")

    if (saved) {
        suggestedPet.value = JSON.parse(saved)
        isFinished.value = true

        // restore scroll
        // setTimeout(() => {
        //     window.scrollTo(0, 300)
        // }, 50)
    }
})

const questions = [
    {
        key: "type",
        category: "Loại thú cưng",
        subtitle: "Chọn giữa chó hoặc mèo",
        text: "Bạn muốn nuôi gì?",
        options: [
            { text: "Chó", value: "dog" },
            { text: "Mèo", value: "cat" }
        ]
    },
    {
        key: "energy",
        category: "Mức năng lượng",
        subtitle: "Ảnh hưởng đến việc vận động mỗi ngày",
        text: "Bạn thích thú cưng vận động mức nào?",
        options: [
            { text: "Ít vận động", value: 1 },
            { text: "Trung bình", value: 3 },
            { text: "Rất năng động", value: 5 }
        ]
    },
    {
        key: "space",
        category: "Không gian sống",
        subtitle: "Phù hợp với diện tích nhà",
        text: "Không gian sống của bạn?",
        options: [
            { text: "Nhỏ", value: 1 },
            { text: "Vừa", value: 3 },
            { text: "Rộng", value: 5 }
        ]
    },
    {
        key: "grooming",
        category: "Chăm sóc",
        subtitle: "Thời gian bạn dành để chăm thú cưng",
        text: "Bạn có thể chăm sóc lông mức nào?",
        options: [
            { text: "Ít chăm", value: 1 },
            { text: "Bình thường", value: 3 },
            { text: "Chăm kỹ", value: 5 }
        ]
    },
    {
        key: "kid_friendly",
        category: "Gia đình",
        subtitle: "Mức độ thân thiện với trẻ nhỏ",
        text: "Nhà bạn có trẻ nhỏ không?",
        options: [
            { text: "Có, cần rất hiền", value: 1 },
            { text: "Không quan trọng", value: 3 },
            { text: "Không có trẻ", value: 5 }
        ]
    },
    {
        key: "size",
        category: "Kích thước",
        subtitle: "Chọn kích thước thú cưng mong muốn",
        text: "Bạn thích kích thước nào?",
        options: [
            { text: "Nhỏ", value: "small" },
            { text: "Trung bình", value: "medium" },
            { text: "Lớn", value: "large" }
        ]
    }
]

const currentStep = ref(0)
const answers = ref({})
const isFinished = ref(false)
const suggestedPet = ref([])

const progress = computed(() => {
    return ((currentStep.value + 1) / questions.length) * 100
})

const selectOption = (val) => {
    const key = questions[currentStep.value].key
    answers.value[key] = val
}

const nextStep = () => {
    const key = questions[currentStep.value].key

    if (answers.value[key]) {
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
    calculateResult()
    isFinished.value = true
}

// 
const WEIGHTS = {
    energy: 2.0,
    space: 1.5,
    grooming: 1.0,
    kid_friendly: 1.5
}

const getVector = (obj) => [
    obj.energy,
    obj.space,
    obj.grooming,
    obj.kid_friendly
]

const weightedDistance = (a, b) => {
    const keys = ["energy", "space", "grooming", "kid_friendly"]

    return Math.sqrt(
        keys.reduce((sum, key, i) => {
            const w = WEIGHTS[key] || 1
            return sum + w * Math.pow(a[i] - b[i], 2)
        }, 0)
    )
}

const calculateResult = () => {

    const filteredPets = allPets
        .filter(p => p.id !== "unknown")
        .filter(p => p.type.toLowerCase() === answers.value.type)

    const userVec = getVector(answers.value)

    let results = []

    filteredPets.forEach(pet => {

        // HARD FILTER
        if (answers.value.space === 1 && pet.scores.space >= 4) return
        if (answers.value.kid_friendly === 1 && pet.scores.kid_friendly >= 4) return

        const petVec = getVector(pet.scores)

        let distance = weightedDistance(userVec, petVec)

        // size penalty
        if (pet.size !== answers.value.size) {
            distance += 1.5
        }

        let score = 100 / (1 + distance)

        results.push({
            pet,
            score,
            distance
        })
    })

    if (results.length === 0) {
        suggestedPet.value = []
        return
    }

    // sort theo score (cao → tốt)
    results.sort((a, b) => b.score - a.score)

    const topPets = results.slice(0, 3)

    suggestedPet.value = topPets.map(item => {

        const pet = item.pet
        const user = answers.value

        let reasons = []

        // Energy
        if (Math.abs(pet.scores.energy - user.energy) <= 1) {
            reasons.push("Mức năng lượng phù hợp với bạn")
        }

        // Space
        if (Math.abs(pet.scores.space - user.space) <= 1) {
            reasons.push("Phù hợp với không gian sống")
        }

        // Grooming
        if (Math.abs(pet.scores.grooming - user.grooming) <= 1) {
            reasons.push("Dễ chăm sóc theo nhu cầu của bạn")
        }

        // Kid
        if (Math.abs(pet.scores.kid_friendly - user.kid_friendly) <= 1) {
            reasons.push("Thân thiện với gia đình/trẻ nhỏ")
        }

        // Size
        if (pet.size === user.size) {
            reasons.push("Kích thước đúng mong muốn")
        }

        return {
            name: pet.name,
            match: Math.round(item.score) + "%",
            image: pet.image_path,
            id: pet.id,
            desc: reasons.slice(0, 2).join(" • "), // lấy 2 lý do đẹp nhất
            fullReasons: reasons // để mở rộng nếu cần
        }
    })
    localStorage.setItem("pet_recommend_results", JSON.stringify(suggestedPet.value))
}

const restart = () => {
    currentStep.value = 0
    answers.value = {}
    isFinished.value = false
    suggestedPet.value = []
}
</script>

<template>
    <div class="pt-32 pb-20 px-4 min-h-screen flex flex-col items-center">

        <!-- Progress Header -->
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

        <!-- Quiz Card -->
        <div v-if="!isFinished"
            class="max-w-2xl w-full bg-white rounded-[2rem] shadow-xl shadow-slate-200/50 overflow-hidden p-6 md:p-10 border border-slate-100 relative">
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
                            :class="answers[questions[currentStep].key] === opt.value ? 'border-teal-500 bg-teal-50' : 'border-slate-100 hover:border-teal-400 hover:bg-teal-50/30'">
                            <div>
                                <p class="font-bold text-base text-slate-800"
                                    :class="answers[questions[currentStep].key] === opt.value ? 'text-teal-800' : ''">{{
                                        opt.text }}
                                </p>
                                <p class="text-xs text-slate-400">{{ opt.sub }}</p>
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
                        <button @click="nextStep" :disabled="!answers[questions[currentStep].key]"
                            class="bg-orange-500 text-white px-10 py-4 rounded-2xl font-black shadow-lg shadow-orange-500/30 hover:bg-orange-600 hover:-translate-y-1 transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                            {{ currentStep === questions.length - 1 ? 'HOÀN TẤT' : 'TIẾP THEO' }}
                        </button>
                    </div>
                </div>
            </transition>
        </div>

        <!-- Result Card -->
        <div v-else class="max-w-4xl w-full text-center">
            <h2 class="text-3xl font-extrabold text-slate-900 mb-2">Kết quả phân tích</h2>
            <p class="text-slate-500 mb-8">Top 3 thú cưng phù hợp với bạn</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div v-for="(pet, index) in suggestedPet" :key="pet.id"
                    class="bg-white rounded-3xl p-6 shadow-xl border relative">

                    <!-- TOP badge -->
                    <div v-if="index === 0"
                        class="absolute -top-3 left-1/2 -translate-x-1/2 bg-orange-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                        Lựa chọn tốt nhất
                    </div>

                    <div class="text-sm text-teal-600 font-bold mb-2">
                        Xác suất: {{ pet.match }}
                    </div>

                    <div class="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4">
                        <img :src="pet.image" class="w-full h-full object-cover">
                    </div>

                    <h3 class="text-xl font-bold mb-2 min-h-[56px] leading-tight">
                        {{ pet.name }}
                    </h3>

                    <p class="text-sm text-slate-500 mb-4 min-h-[40px]">
                        {{ pet.desc }}
                    </p>

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
