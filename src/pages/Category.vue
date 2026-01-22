<script setup>
import { ref, computed } from 'vue'
import { Search, ChevronLeft, ChevronRight, Filter, Dog, Cat, X } from 'lucide-vue-next'
import { allPets } from '../data/pets'
import PetCard from '../components/PetCard.vue'

// State
const searchQuery = ref('')
const selectedType = ref('All') // 'All', 'Dog', 'Cat'
const selectedSize = ref('All')
const priceRange = ref([0, 50]) // Min 0, Max 50 (Million)
const currentPage = ref(1)
const itemsPerPage = 6
const showMobileFilters = ref(false)

// Computed
const filteredPets = computed(() => {
  return allPets.filter(pet => {
    const matchesSearch = pet.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = selectedType.value === 'All' || pet.type === selectedType.value
    const matchesSize = selectedSize.value === 'All' || pet.size === selectedSize.value
    const matchesPrice = pet.priceMin >= priceRange.value[0] && pet.priceMax <= priceRange.value[1]
    
    return matchesSearch && matchesType && matchesSize && matchesPrice
  })
})

const totalPages = computed(() => Math.ceil(filteredPets.value.length / itemsPerPage))

const paginatedPets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredPets.value.slice(start, end)
})

const activeFiltersCount = computed(() => {
    let count = 0
    if (selectedType.value !== 'All') count++
    if (selectedSize.value !== 'All') count++
    if (priceRange.value[0] > 0 || priceRange.value[1] < 50) count++
    return count
})

// Methods
const setPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const clearFilters = () => {
    selectedType.value = 'All'
    selectedSize.value = 'All'
    priceRange.value = [0, 50]
    searchQuery.value = ''
    currentPage.value = 1
}
</script>

<template>
  <div class="pt-32 pb-20 px-4 min-h-screen bg-slate-50">
    <div class="max-w-[1400px] mx-auto">
      
      <!-- Header Section -->
      <div class="text-center mb-16">
        <h1 class="text-5xl md:text-6xl font-black text-slate-900 mb-6 tracking-tight">Thư viện <span class="text-teal-600">Thú Cưng</span></h1>
        <p class="text-xl md:text-2xl text-slate-500 font-medium max-w-2xl mx-auto">Khám phá thông tin chi tiết về hàng trăm giống chó mèo phổ biến nhất hiện nay.</p>
      </div>

      <div class="flex flex-col lg:flex-row gap-8 items-start">
        
        <!-- Sidebar Filters (Desktop) -->
        <aside class="w-full lg:w-80 bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm shrink-0 sticky top-28 hidden lg:block">
            <div class="flex items-center justify-between mb-8">
                <h3 class="text-2xl font-extrabold text-slate-900 flex items-center gap-2">
                    <Filter class="w-6 h-6 text-teal-600"/> Bộ lọc
                </h3>
                <button v-if="activeFiltersCount > 0" @click="clearFilters" class="text-sm font-bold text-orange-500 hover:underline">
                    Xóa tất cả
                </button>
            </div>

            <!-- Type Filter -->
            <div class="mb-8">
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Loài vật</label>
                <div class="grid grid-cols-3 gap-2">
                    <button 
                        v-for="type in ['All', 'Dog', 'Cat']" 
                        :key="type"
                        @click="selectedType = type; currentPage=1"
                        class="flex flex-col items-center justify-center p-3 rounded-2xl border-2 transition-all"
                        :class="selectedType === type ? 'border-teal-500 bg-teal-50 text-teal-700' : 'border-slate-100 hover:border-teal-200 text-slate-500'"
                    >
                        <span v-if="type==='All'" class="font-bold text-lg">Tất cả</span>
                        <Dog v-if="type==='Dog'" class="w-6 h-6 mb-1"/>
                        <Cat v-if="type==='Cat'" class="w-6 h-6 mb-1"/>
                        <span v-if="type!=='All'" class="text-xs font-bold">{{ type==='Dog' ? 'Chó' : 'Mèo' }}</span>
                    </button>
                </div>
            </div>

            <!-- Size Filter -->
            <div class="mb-8">
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Kích thước</label>
                <div class="space-y-2">
                    <button 
                        v-for="size in ['All', 'Nhỏ', 'Trung bình', 'Lớn']"
                        :key="size" 
                        @click="selectedSize = size; currentPage=1"
                        class="w-full text-left px-4 py-3 rounded-xl font-bold transition-all flex justify-between items-center"
                        :class="selectedSize === size ? 'bg-teal-600 text-white shadow-lg shadow-teal-500/30' : 'bg-slate-50 text-slate-600 hover:bg-slate-100'"
                    >
                        {{ size === 'All' ? 'Tất cả kích thước' : size }}
                        <span v-if="selectedSize === size" class="bg-white/20 w-5 h-5 rounded-full flex items-center justify-center text-xs">✓</span>
                    </button>
                </div>
            </div>

            <!-- Price Range -->
            <div>
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Mức giá (Triệu VNĐ)</label>
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-slate-100 px-4 py-2 rounded-xl font-bold text-slate-700 w-full text-center">{{ priceRange[0] }}M</div>
                    <span class="font-bold text-slate-300">-</span>
                    <div class="bg-slate-100 px-4 py-2 rounded-xl font-bold text-slate-700 w-full text-center">{{ priceRange[1] }}M</div>
                </div>
                <input 
                    type="range" v-model.number="priceRange[0]" min="0" max="50" step="1" 
                    class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600 mb-2"
                >
                <input 
                    type="range" v-model.number="priceRange[1]" min="0" max="100" step="1" 
                    class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
                >
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 w-full">
            
            <!-- Mobile Filter Toggle -->
            <div class="lg:hidden mb-6 flex gap-4">
                <div class="relative w-full group">
                    <Search class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
                    <input 
                        v-model="searchQuery"
                        type="text" 
                        placeholder="Tìm kiếm..." 
                        class="w-full bg-white border border-slate-200 rounded-2xl py-4 pl-12 pr-4 shadow-sm focus:ring-2 focus:ring-teal-500 font-bold text-lg"
                    >
                </div>
                <button 
                    @click="showMobileFilters = true"
                    class="bg-white border border-slate-200 p-4 rounded-2xl shadow-sm text-slate-700 relative"
                >
                    <Filter class="w-6 h-6"/>
                    <span v-if="activeFiltersCount > 0" class="absolute -top-2 -right-2 bg-orange-500 text-white w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center border-2 border-white">
                        {{ activeFiltersCount }}
                    </span>
                </button>
            </div>

            <!-- Desktop Search Bar -->
            <div class="hidden lg:block relative w-full mb-8">
                <Search class="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 w-6 h-6 group-focus-within:text-teal-600 transition" />
                <input 
                    v-model="searchQuery"
                    type="text" 
                    placeholder="Tìm kiếm tên giống thú cưng..." 
                    class="w-full bg-white border-2 border-slate-100 rounded-[2rem] py-5 pl-16 pr-6 shadow-sm focus:border-teal-500 focus:ring-0 transition-all font-bold text-xl text-slate-800 placeholder-slate-400"
                >
            </div>

            <!-- Pet Grid -->
            <div v-if="filteredPets.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 mb-12">
                <PetCard v-for="pet in paginatedPets" :key="pet.id" :pet="pet" />
            </div>

            <!-- No Results -->
            <div v-else class="text-center py-20 bg-white rounded-[2rem] border-2 border-dashed border-slate-200">
                <p class="text-2xl text-slate-400 font-bold mb-4">Không tìm thấy kết quả nào!</p>
                <button @click="clearFilters" class="px-8 py-3 bg-teal-100 text-teal-700 font-bold rounded-xl hover:bg-teal-200 transition">
                    Xóa bộ lọc
                </button>
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-12">
                <button 
                    @click="setPage(currentPage - 1)" 
                    class="w-12 h-12 rounded-2xl flex items-center justify-center border-2 border-slate-200 hover:border-teal-400 hover:text-teal-600 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
                    :disabled="currentPage === 1"
                >
                    <ChevronLeft class="w-6 h-6" />
                </button>

                <button 
                    v-for="p in totalPages" 
                    :key="p"
                    @click="setPage(p)"
                    class="w-12 h-12 rounded-2xl font-black text-lg transition border-2"
                    :class="currentPage === p ? 'bg-teal-600 text-white border-teal-600 shadow-lg shadow-teal-600/30' : 'bg-white text-slate-500 border-slate-200 hover:border-teal-400 hover:text-teal-600'"
                >
                    {{ p }}
                </button>

                <button 
                    @click="setPage(currentPage + 1)" 
                    class="w-12 h-12 rounded-2xl flex items-center justify-center border-2 border-slate-200 hover:border-teal-400 hover:text-teal-600 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
                    :disabled="currentPage === totalPages"
                >
                    <ChevronRight class="w-6 h-6" />
                </button>
            </div>
        </main>

      </div>
    
    </div>

    <!-- Mobile Filter Drawer -->
    <div v-if="showMobileFilters" class="fixed inset-0 z-50 lg:hidden">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showMobileFilters = false"></div>
        <div class="absolute right-0 top-0 bottom-0 w-80 bg-white shadow-2xl p-6 overflow-y-auto">
            <div class="flex items-center justify-between mb-8">
                <h3 class="text-2xl font-black text-slate-900">Bộ lọc</h3>
                <button @click="showMobileFilters = false" class="p-2 bg-slate-100 rounded-full hover:bg-slate-200">
                    <X class="w-6 h-6 text-slate-600"/>
                </button>
            </div>
            
            <!-- Mobile Filters Content (Same as Desktop Sidebar but adapted) -->
             <div class="mb-8">
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Loài vật</label>
                <div class="grid grid-cols-3 gap-2">
                    <button 
                        v-for="type in ['All', 'Dog', 'Cat']" 
                        :key="type"
                        @click="selectedType = type; currentPage=1"
                        class="flex flex-col items-center justify-center p-3 rounded-2xl border-2 transition-all"
                        :class="selectedType === type ? 'border-teal-500 bg-teal-50 text-teal-700' : 'border-slate-100 hover:border-teal-200 text-slate-500'"
                    >
                        <span v-if="type==='All'" class="font-bold text-lg">Tất cả</span>
                        <Dog v-if="type==='Dog'" class="w-6 h-6 mb-1"/>
                        <Cat v-if="type==='Cat'" class="w-6 h-6 mb-1"/>
                        <span v-if="type!=='All'" class="text-xs font-bold">{{ type==='Dog' ? 'Chó' : 'Mèo' }}</span>
                    </button>
                </div>
            </div>

            <div class="mb-8">
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Kích thước</label>
                <div class="space-y-2">
                    <button 
                        v-for="size in ['All', 'Nhỏ', 'Trung bình', 'Lớn']"
                        :key="size" 
                        @click="selectedSize = size; currentPage=1"
                        class="w-full text-left px-4 py-3 rounded-xl font-bold transition-all flex justify-between items-center"
                        :class="selectedSize === size ? 'bg-teal-600 text-white' : 'bg-slate-50 text-slate-600'"
                    >
                        {{ size === 'All' ? 'Tất cả' : size }}
                        <span v-if="selectedSize === size" class="bg-white/20 w-5 h-5 rounded-full flex items-center justify-center text-xs">✓</span>
                    </button>
                </div>
            </div>

            <div class="mb-8">
                <label class="block text-sm font-black text-slate-400 uppercase tracking-wider mb-4">Mức giá</label>
                <div class="flex items-center gap-2 mb-4">
                    <div class="bg-slate-100 px-3 py-2 rounded-xl font-bold text-slate-700 w-full text-center">{{ priceRange[0] }}M</div>
                    <span class="font-bold text-slate-300">-</span>
                    <div class="bg-slate-100 px-3 py-2 rounded-xl font-bold text-slate-700 w-full text-center">{{ priceRange[1] }}M</div>
                </div>
                <input type="range" v-model.number="priceRange[0]" min="0" max="50" class="w-full mb-2">
                <input type="range" v-model.number="priceRange[1]" min="0" max="100" class="w-full">
            </div>

             <button @click="clearFilters(); showMobileFilters = false" class="w-full py-4 text-orange-500 font-bold border-2 border-orange-100 rounded-xl">
                    Xóa bộ lọc
            </button>
        </div>
    </div>

  </div>
</template>
