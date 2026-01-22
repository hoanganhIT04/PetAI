<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { allPets } from '../data/pets'
import { ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const pet = computed(() => {
    const id = parseInt(route.params.id)
    return allPets.find(p => p.id === id) || allPets[0] // Fallback if not found
})
</script>

<template>
  <div class="pt-32 pb-20 px-4 max-w-6xl mx-auto">
    
    <RouterLink to="/category" class="inline-flex items-center gap-2 text-slate-500 font-bold hover:text-teal-600 mb-8 transition">
        <ArrowLeft class="w-5 h-5"/> Quay lại thư viện
    </RouterLink>

    <div class="bg-white rounded-[2.5rem] overflow-hidden shadow-2xl border border-slate-100 flex flex-col md:flex-row">
      
      <!-- Image Side -->
      <div class="md:w-1/2 h-96 md:h-[600px] relative">
        <img :src="pet.img" class="w-full h-full object-cover">
        <div class="absolute top-6 left-6 bg-white/90 backdrop-blur px-4 py-2 rounded-full font-bold text-teal-700 shadow-sm flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
            #{{ pet.id }} Phổ biến
        </div>
      </div>

      <!-- Content Side -->
      <div class="md:w-1/2 p-10 md:p-14 flex flex-col justify-between">
        <div class="space-y-8">
            <div>
                <h1 class="text-4xl md:text-5xl font-black text-slate-900 leading-tight mb-2">{{ pet.name }}</h1>
                <p class="text-orange-500 font-bold text-2xl">{{ pet.price }}</p>
            </div>

            <p class="text-slate-500 leading-relaxed text-lg">
                {{ pet.name }} là giống thú cưng được yêu thích bởi tính cách thân thiện và ngoại hình đáng yêu.
                Chúng rất phù hợp với các gia đình có trẻ nhỏ và có khả năng thích nghi tốt với môi trường sống.
            </p>

            <div class="grid grid-cols-2 gap-4">
                <div class="bg-teal-50 p-5 rounded-2xl border border-teal-100">
                    <span class="text-[10px] font-black text-teal-600 uppercase tracking-wider">Tuổi thọ trung bình</span>
                    <p class="text-xl font-bold text-slate-800 mt-1">{{ pet.age }}</p>
                </div>
                <div class="bg-orange-50 p-5 rounded-2xl border border-orange-100">
                    <span class="text-[10px] font-black text-orange-600 uppercase tracking-wider">Kích thước</span>
                    <p class="text-xl font-bold text-slate-800 mt-1">{{ pet.size }}</p>
                </div>
            </div>

            <div class="space-y-5 pt-4">
                <div class="space-y-2">
                    <div class="flex justify-between text-xs font-bold uppercase text-slate-500"><span>Mức năng lượng</span><span>70%</span></div>
                    <div class="h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-teal-500 h-full w-[70%]"></div></div>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between text-xs font-bold uppercase text-slate-500"><span>Dễ huấn luyện</span><span>90%</span></div>
                    <div class="h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-orange-500 h-full w-[90%]"></div></div>
                </div>
            </div>
        </div>

        <button class="w-full mt-10 bg-slate-900 text-white py-4 rounded-2xl font-bold hover:bg-teal-700 transition shadow-xl transform active:scale-[0.98]">
            Liên hệ tư vấn nuôi
        </button>
      </div>
    </div>
  </div>
</template>
