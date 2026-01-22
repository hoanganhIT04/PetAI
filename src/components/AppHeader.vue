<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { Dog, Cat, ScanLine, Heart, BookOpen, CheckCircle } from 'lucide-vue-next'

const route = useRoute()
</script>

<template>
  <header class="fixed w-full top-0 left-0 z-50 transition-all duration-300 glass border-b border-slate-200" id="main-header">
    <div class="max-w-7xl mx-auto px-4 h-24 grid grid-cols-3 items-center">
      
      <!-- Logo (Left) -->
      <RouterLink to="/" class="flex items-center gap-3 group justify-self-start">
        <div class="relative w-10 h-10 bg-teal-600 rounded-xl flex items-center justify-center shadow-lg group-hover:rotate-12 transition-transform">
          <Dog class="text-white w-6 h-6 absolute transition-all duration-300 group-hover:scale-0" />
          <Cat class="text-white w-6 h-6 absolute transition-all duration-300 scale-0 group-hover:scale-100" />
        </div>
        <span class="text-xl font-extrabold text-slate-800 tracking-tight">Pet<span class="text-teal-600">AI</span></span>
      </RouterLink>

      <!-- Desktop Nav (Center) -->
      <nav class="hidden md:flex items-center gap-8 bg-white/50 px-8 py-3 rounded-full border border-slate-100 shadow-sm backdrop-blur-md justify-self-center">
        <RouterLink to="/" 
          class="flex items-center gap-2 text-sm font-medium transition-all duration-300 text-slate-500 hover:text-teal-600"
          active-class="text-teal-600 font-bold bg-teal-50/50 px-3 py-1 rounded-lg"
        >
          Trang chủ
        </RouterLink>
        <RouterLink to="/category" 
          class="flex items-center gap-2 text-sm font-medium transition-all duration-300 text-slate-500 hover:text-teal-600"
          active-class="text-teal-600 font-bold bg-teal-50/50 px-3 py-1 rounded-lg"
        >
          Thư viện
        </RouterLink>
        <RouterLink to="/matching" 
          class="flex items-center gap-2 text-sm font-medium transition-all duration-300 text-slate-500 hover:text-teal-600"
          active-class="text-teal-600 font-bold bg-teal-50/50 px-3 py-1 rounded-lg"
        >
          Ghép đôi
        </RouterLink>
      </nav>

      <!-- CTA Button (Right) -->
      <div class="justify-self-end">
        <button class="bg-slate-900 text-white px-5 py-2.5 rounded-xl font-bold text-sm hover:bg-teal-600 hover:shadow-lg hover:shadow-teal-600/20 transition-all duration-300 flex items-center gap-2 group">
          <ScanLine class="w-4 h-4 transition-transform group-hover:scale-110" />
          <span>Tải App</span>
        </button>
      </div>

    </div>
  </header>
  <!-- Spacer for fixed header -->
  <div class="h-24"></div>
</template>

<style scoped>
.glass {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}
</style>
