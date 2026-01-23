<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import allPets from '../data/pets_data.json'
import { ArrowLeft, Activity, Home, Scissors, Heart, DollarSign } from 'lucide-vue-next'

const route = useRoute()

// Computed
const pet = computed(() => {
    // Route param is string, JSON id is string (slug).
    const slug = route.params.id
    const foundPet = allPets.find(p => p.id === slug)
    
    // Fallback or Not Found handling
    // For now, if not found, return null and we show a "Not Found" UI
    return foundPet || null
})

// Star rating component helper logic
const getStarCount = (score) => {
    // Score is 1-3. Let's map to 5 scale visually or just display bars.
    // User asked for Progress Bars or Star Icons.
    // Score 3 -> 5 stars (Excellent)
    // Score 2 -> 3 stars (Average)
    // Score 1 -> 1-2 stars (Low) or reverse depending on meaning.
    // Actually simplicity: Just show x/3 dots or bars.
    return score
}
</script>

<template>
  <div class="pt-24 pb-16 px-4 min-h-screen bg-slate-50">
    <div class="max-w-6xl mx-auto">
        
        <!-- Back Button -->
        <RouterLink to="/category" class="inline-flex items-center gap-2 text-slate-500 font-bold hover:text-teal-600 mb-8 transition group">
            <div class="bg-white p-2 rounded-xl shadow-sm border border-slate-100 group-hover:bg-teal-50 group-hover:border-teal-100 transition">
                <ArrowLeft class="w-5 h-5"/> 
            </div>
            Quay lại thư viện
        </RouterLink>

        <!-- Not Found State -->
        <div v-if="!pet" class="text-center py-20 bg-white rounded-[2rem] border-2 border-dashed border-slate-200">
            <h2 class="text-3xl font-black text-slate-400 mb-2">Không tìm thấy thông tin!</h2>
            <p class="text-slate-500 mb-6">Có vẻ như giống thú cưng này không tồn tại trong dữ liệu của chúng tôi.</p>
            <RouterLink to="/category" class="px-6 py-3 bg-teal-600 text-white font-bold rounded-xl hover:bg-teal-700">
                Khám phá thú cưng khác
            </RouterLink>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            <!-- Left Column: Image & Quick Stats (lg:col-span-5) -->
            <div class="lg:col-span-5 space-y-6 sticky top-24">
                <div class="bg-white rounded-[2.5rem] overflow-hidden shadow-xl border border-slate-100 relative group h-[400px] lg:h-[500px]">
                    <img 
                        :src="pet.image_path" 
                        class="w-full h-full object-cover transition duration-700 group-hover:scale-105"
                        @error="$event.target.src = '/assets/placeholder_pet.jpg'"
                    >
                    
                    <div class="absolute top-6 left-6 flex flex-wrap gap-2">
                        <span class="bg-white/90 backdrop-blur px-4 py-2 rounded-full font-black text-teal-700 shadow-sm text-xs uppercase tracking-wider">
                            {{ pet.type === 'Dog' ? 'Chó cảnh' : 'Mèo cảnh' }}
                        </span>
                        <span class="bg-orange-500/90 backdrop-blur px-4 py-2 rounded-full font-black text-white shadow-sm text-xs uppercase tracking-wider">
                            Size: {{ pet.size }}
                        </span>
                    </div>
                </div>

                <!-- Scores Grid -->
                <div class="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
                    <h3 class="text-lg font-black text-slate-900 mb-4 flex items-center gap-2">
                        <Activity class="w-5 h-5 text-teal-500"/> Chỉ số đặc điểm
                    </h3>
                    <div class="grid grid-cols-2 gap-4">
                        <!-- Score Item -->
                        <div class="bg-slate-50 p-4 rounded-2xl">
                            <div class="flex items-center gap-2 text-slate-500 text-xs font-bold uppercase mb-2">
                                <Activity class="w-4 h-4"/> Vận động
                            </div>
                            <div class="flex gap-1">
                                <span v-for="i in 3" :key="i" class="h-2 w-full rounded-full" :class="i <= pet.scores?.energy ? 'bg-teal-500' : 'bg-slate-200'"></span>
                            </div>
                        </div>

                         <div class="bg-slate-50 p-4 rounded-2xl">
                            <div class="flex items-center gap-2 text-slate-500 text-xs font-bold uppercase mb-2">
                                <Home class="w-4 h-4"/> Không gian
                            </div>
                            <div class="flex gap-1">
                                <span v-for="i in 3" :key="i" class="h-2 w-full rounded-full" :class="i <= pet.scores?.space ? 'bg-blue-500' : 'bg-slate-200'"></span>
                            </div>
                        </div>

                         <div class="bg-slate-50 p-4 rounded-2xl">
                            <div class="flex items-center gap-2 text-slate-500 text-xs font-bold uppercase mb-2">
                                <Scissors class="w-4 h-4"/> Chăm sóc lông
                            </div>
                            <div class="flex gap-1">
                                <span v-for="i in 3" :key="i" class="h-2 w-full rounded-full" :class="i <= pet.scores?.grooming ? 'bg-purple-500' : 'bg-slate-200'"></span>
                            </div>
                        </div>

                         <div class="bg-slate-50 p-4 rounded-2xl">
                            <div class="flex items-center gap-2 text-slate-500 text-xs font-bold uppercase mb-2">
                                <Heart class="w-4 h-4"/> Thân thiện trẻ em
                            </div>
                            <div class="flex gap-1">
                                <span v-for="i in 3" :key="i" class="h-2 w-full rounded-full" :class="i <= pet.scores?.kid_friendly ? 'bg-red-500' : 'bg-slate-200'"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Details & Content (lg:col-span-7) -->
            <div class="lg:col-span-7 space-y-8">
                
                <!-- Title Section -->
                <div>
                     <h1 class="text-4xl md:text-5xl font-black text-slate-900 mb-4 tracking-tight">{{ pet.name }}</h1>
                     <div class="flex items-center gap-4 text-slate-500 font-bold text-lg">
                        <span class="flex items-center gap-2 bg-white px-4 py-2 rounded-xl border border-slate-100 shadow-sm">
                            ⏳ Tuổi thọ: {{ pet.lifespan }}
                        </span>
                     </div>
                </div>
                
                <!-- Pricing Card -->
                <div class="bg-gradient-to-br from-teal-600 to-teal-800 rounded-3xl p-8 text-white shadow-xl shadow-teal-900/20 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
                    
                    <h3 class="text-xl font-bold mb-6 flex items-center gap-2 border-b border-white/20 pb-4">
                        <DollarSign class="w-6 h-6"/> Bảng giá tham khảo
                    </h3>
                    
                    <div class="space-y-4 relative z-10">
                        <div class="flex flex-col md:flex-row md:items-center justify-between bg-white/10 p-4 rounded-2xl border border-white/10">
                            <span class="text-teal-100 font-medium mb-1 md:mb-0">Có giấy tờ (VKA)</span>
                            <span class="text-2xl font-black">{{ pet.price.paper }}</span>
                        </div>
                         <div class="flex flex-col md:flex-row md:items-center justify-between bg-white/5 p-4 rounded-2xl border border-white/5">
                            <span class="text-teal-200 font-medium mb-1 md:mb-0">Không giấy tờ</span>
                            <span class="text-xl font-bold">{{ pet.price.no_paper }}</span>
                        </div>
                         <div class="flex flex-col md:flex-row md:items-center justify-between bg-white/5 p-4 rounded-2xl border border-white/5">
                            <span class="text-teal-200 font-medium mb-1 md:mb-0">Nhập khẩu (Quốc tế)</span>
                            <span class="text-xl font-bold">{{ pet.price.international }}</span>
                        </div>
                    </div>
                </div>

                <!-- Care Instructions -->
                <div class="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
                    <h3 class="text-2xl font-black text-slate-900 mb-6">Hướng dẫn chăm sóc</h3>
                    <div class="prose prose-slate prose-lg max-w-none">
                        <p class="whitespace-pre-line text-slate-600 leading-relaxed">
                            {{ pet.care_instruction }}
                        </p>
                    </div>
                </div>

                <!-- CTA -->
                <div class="bg-orange-50 rounded-3xl p-8 flex flex-col md:flex-row items-center justify-between gap-6 border border-orange-100">
                    <div>
                        <h4 class="text-xl font-black text-slate-900 mb-2">Bạn quan tâm đến {{ pet.name }}?</h4>
                        <p class="text-slate-600">Liên hệ với chúng tôi để được tư vấn chi tiết về cách nuôi và chăm sóc.</p>
                    </div>
                    <button class="px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-xl shadow-lg shadow-orange-500/30 transition transform hover:-translate-y-1">
                        Liên hệ ngay
                    </button>
                </div>

            </div>
        </div>

    </div>
  </div>
</template>
