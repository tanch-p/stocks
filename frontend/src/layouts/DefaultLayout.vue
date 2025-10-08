<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

const route = useRoute()
const basePath = computed(() => route.fullPath.split(/[?#]/)[0])

const hideNavbar = computed(() => basePath.value === '/login')
</script>

<template>
  <Header />
  <div>
    <AppNavbar v-if="!hideNavbar" />
    <router-view />
  </div>
  <Footer />
</template>
