<script setup>
import { Clock, ChevronRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const props = defineProps({
  pet: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/info/${props.pet.id}`)
}
</script>

<template>
  <div 
    class="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-100 pet-card group cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1" 
    @click="goToDetail"
  >
    <div class="h-48 overflow-hidden relative">
      <img 
        :src="pet.image_path" 
        class="w-full h-full object-cover group-hover:scale-110 transition duration-500" 
        alt="Pet Image"
        @error="$event.target.src = '/assets/placeholder_pet.jpg'"
      >
      <div class="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-[10px] font-black uppercase text-teal-600 shadow-sm">
        {{ pet.size }}
      </div>
       <div class="absolute bottom-2 left-2 flex gap-1">
            <!-- Invert Kid Friendly Score for Display: 1(Safe) -> 5 Stars, 5(Risk) -> 1 Star -->
            <span v-for="i in 5" :key="i" class="text-xs" :class="i <= (6 - (pet.scores?.kid_friendly || 3)) ? 'text-yellow-400' : 'text-gray-300'">
                ★
            </span>
       </div>
    </div>
    <div class="p-5">
      <div class="flex justify-between items-start mb-1">
        <h3 class="font-bold text-lg text-slate-900 line-clamp-1" :title="pet.name">{{ pet.name }}</h3>
      </div>
      
      <div class="flex items-center gap-3 text-slate-500 text-xs mb-3">
        <span class="flex items-center gap-1"><Clock class="w-3 h-3" /> {{ pet.lifespan }}</span>
      </div>

       <!-- Badges for Scores -->
      <div class="flex gap-2 mb-3 text-[10px] font-bold">
           <span class="px-2 py-1 rounded-md bg-blue-50 text-blue-600 border border-blue-100">
               Energy: {{ pet.scores?.energy }}/5
           </span>
           <span class="px-2 py-1 rounded-md bg-purple-50 text-purple-600 border border-purple-100">
               Space: {{ pet.scores?.space }}/5
           </span>
      </div>

      <div class="flex items-center justify-between border-t border-slate-100 pt-3">
        <span class="text-orange-500 font-bold text-sm">{{ pet.price?.paper || 'Liên hệ' }}</span>
        <span class="text-teal-600 text-xs font-bold flex items-center gap-1 group-hover:underline underline-offset-4">
          Chi tiết <ChevronRight class="w-3 h-3" />
        </span>
      </div>
    </div>
  </div>
</template>
