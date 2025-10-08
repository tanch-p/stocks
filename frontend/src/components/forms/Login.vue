<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const mode = ref('password')
const message = ref('')
const otp = ref('')

function toggleMode() {
  mode.value = mode.value === 'password' ? 'otp' : 'password'
}

async function login() {
  message.value = ''
  otp.value = ''
  const payload = { email: email.value }
  if (mode.value === 'password') payload.password = password.value

  const res = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const data = await res.json()

  if (res.ok) {
    if (mode.value === 'otp') {
      message.value = data.message
      otp.value = data.otp_demo // dev only
    } else {
      localStorage.setItem('token', data.access_token)
      message.value = 'Login successful!'
    }
  } else {
    message.value = data.detail || 'Login failed'
  }
}
</script>


<template>
  <div class="max-w-sm mx-auto p-6 bg-white rounded-2xl shadow">
    <h2 class="text-xl font-bold mb-4 text-center">Login</h2>

    <form @submit.prevent="login">
      <div class="mb-3">
        <label class="block text-sm mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded p-2" required />
      </div>

      <div v-if="mode === 'password'" class="mb-3">
        <label class="block text-sm mb-1">Password</label>
        <input v-model="password" type="password" class="w-full border rounded p-2" required />
      </div>

      <div class="flex justify-between items-center mb-3">
        <span class="text-sm text-gray-500">Mode: {{ mode }}</span>
        <button
          type="button"
          class="text-blue-600 text-sm"
          @click="toggleMode"
        >
          Use {{ mode === 'password' ? 'OTP' : 'Password' }}
        </button>
      </div>

      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
      >
        {{ mode === 'password' ? 'Login' : 'Send OTP' }}
      </button>
    </form>

    <p v-if="message" class="text-green-600 mt-3 text-center">{{ message }}</p>
    <p v-if="otp" class="text-gray-500 mt-1 text-center">Demo OTP: {{ otp }}</p>
  </div>
</template>

