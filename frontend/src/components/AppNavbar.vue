<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import HomeIcon from '@/assets/home.svg'

const route = useRoute()

const basePath = computed(() => route.fullPath.split(/[?#]/)[0])

const paths = [
  { icon: HomeIcon, path: '/', name: 'Home' },
  { icon: HomeIcon, path: '/about', name: 'About' },
  { icon: HomeIcon, path: '/settings', name: 'Settings' },
]
</script>

<template>
  <nav
    class="fixed z-[1] bottom-0 border-t border-light-gray bg-white flex items-center justify-around w-full p-4 text-xs"
  >
    <router-link
      v-for="item in paths"
      :key="item.path"
      :to="item.path"
      :class="{ active: basePath === item.path }"
      class="flex flex-col items-center justify-center"
    >
      <component :is="item.icon" class="" />
      {{ item.name }}
    </router-link>
  </nav>
</template>

<style scoped>
.active {
  color: dodgerblue;
  font-weight: bold;
}
</style>
