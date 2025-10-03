<script setup lang="ts">
import LogoIcon from '@/assets/dollar.svg'
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="py-1">
    <div class="flex items-center justify-between max-w-[1200px] w-full mx-auto px-1.5">
      <div class="flex items-center">
        <LogoIcon class="w-6 h-6 text-black" />
        <h1 class="text-2xl">ILP Fund Tracker</h1>
      </div>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <span>Login</span>
      </nav>
    </div>
  </header>
</template>
