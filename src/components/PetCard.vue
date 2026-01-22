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
      <img :src="pet.img" class="w-full h-full object-cover group-hover:scale-110 transition duration-500" alt="Pet Image">
      <div class="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-[10px] font-black uppercase text-teal-600 shadow-sm">
        {{ pet.size }}
      </div>
    </div>
    <div class="p-5">
      <h3 class="font-bold text-lg text-slate-900 mb-1">{{ pet.name }}</h3>
      <div class="flex items-center gap-3 text-slate-500 text-xs mb-3">
        <span class="flex items-center gap-1"><Clock class="w-3 h-3" /> {{ pet.age }}</span>
      </div>
      <div class="flex items-center justify-between border-t border-slate-100 pt-3">
        <span class="text-orange-500 font-bold">{{ pet.price }}</span>
        <span class="text-teal-600 text-xs font-bold flex items-center gap-1 group-hover:underline underline-offset-4">
          Chi tiết <ChevronRight class="w-3 h-3" />
        </span>
      </div>
    </div>
  </div>
</template>
