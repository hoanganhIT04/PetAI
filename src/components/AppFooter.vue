<script setup>
import { Dog, Mail, Phone, MapPin, Facebook, Instagram, Twitter } from 'lucide-vue-next'
</script>

<template>
  <footer class="bg-white border-t border-slate-100 pt-10 pb-8">
    <div class="max-w-7xl mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
        <div class="space-y-6">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center shadow-lg">
              <Dog class="text-white w-5 h-5" />
            </div>
            <span class="text-xl font-extrabold text-slate-800 tracking-tight">Pet<span class="text-teal-600">AI</span></span>
          </div>
          <p class="text-slate-500 leading-relaxed text-sm">Công nghệ AI tiên tiến giúp bạn thấu hiểu người bạn bốn chân của mình hơn bao giờ hết.</p>
        </div>

        <div>
          <h4 class="font-bold text-slate-900 mb-4 text-base">Liên kết nhanh</h4>
          <ul class="space-y-3 text-sm text-slate-500">
            <li><a href="#" class="hover:text-teal-600 transition">Về chúng tôi</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Công nghệ AI</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Bảng giá</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Blog thú cưng</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-bold text-slate-900 mb-4 text-base">Hỗ trợ</h4>
          <ul class="space-y-3 text-sm text-slate-500">
            <li><a href="#" class="hover:text-teal-600 transition">Trung tâm trợ giúp</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Điều khoản sử dụng</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Chính sách bảo mật</a></li>
            <li><a href="#" class="hover:text-teal-600 transition">Liên hệ</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-bold text-slate-900 mb-4 text-base">Liên hệ</h4>
          <ul class="space-y-3 text-sm text-slate-500">
            <li class="flex items-center gap-2"><Mail class="w-4 h-4 text-teal-600" /> contact@petai.com</li>
            <li class="flex items-center gap-2"><Phone class="w-4 h-4 text-teal-600" /> +84 123 456 789</li>
            <li class="flex items-center gap-2"><MapPin class="w-4 h-4 text-teal-600" /> TP. Hồ Chí Minh, VN</li>
          </ul>
        </div>
      </div>

      <div class="border-t border-slate-100 pt-6 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-slate-400 text-xs">© 2024 PetAI. All rights reserved.</p>
        <div class="flex items-center gap-4">
          <a href="#" class="text-slate-400 hover:text-teal-600 transition"><Facebook class="w-5 h-5" /></a>
          <a href="#" class="text-slate-400 hover:text-pink-600 transition"><Instagram class="w-5 h-5" /></a>
          <a href="#" class="text-slate-400 hover:text-sky-500 transition"><Twitter class="w-5 h-5" /></a>
        </div>
      </div>
    </div>
  </footer>
</template>
