<script setup lang="ts">
import { ref } from 'vue'

const mode = ref('password')
const email = ref('')
const password = ref('')
const otp = ref('')

function changeLoginMode(option: string) {
  mode.value = option
}
</script>

<template>
  <main class="min-h-screen">
    <div class="max-w-[800px] w-full mx-auto py-40">
      <div class="shadow-xs bg-white">
        <div class="border border-light-gray -mt-2 p-4">
          <h3>Welcome back</h3>
          <span>Sign in to your account</span>
          <div class="grid grid-cols-2">
            <button :class="{ active: mode === 'password' }" @click="changeLoginMode('password')">
              <span>Password</span>
              <div
                :class="mode === 'password' ? 'bg-pri-color' : 'bg-none'"
                class="rounded w-full h-[2px] mt-1.5"
              />
            </button>
            <button :class="{ active: mode === 'otp' }" @click="changeLoginMode('otp')">
              <span>OTP</span>
              <div
                :class="mode === 'otp' ? 'bg-pri-color' : 'bg-none'"
                class="rounded w-full h-[2px] mt-1.5"
              />
            </button>
          </div>
          <hr class="border-light-gray" />
        </div>
        <div v-if="mode === 'password'" class="flex flex-col">
          <input v-model="email" placeholder="Email Address" />
          <input v-model="password" placeholder="Password" />
          <button class="text-pri-color">Forgot password?</button>
          <button type="submit" class="rounded bg-pri-color py-1.5 text-white">Sign In</button>
        </div>
        <div v-if="mode === 'otp'" class="flex flex-col">
          <input v-model="email" placeholder="Email Address" />
        </div>
        <div>
          Don't have an account?
          <router-link :to="'/forgot-password'" class="text-pri-color"> Sign Up</router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  background: linear-gradient(135deg, #e0f2f1, #ffffff);
}
button.active {
  font-weight: 600;
}
</style>
