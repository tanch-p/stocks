<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const otp = ref('')
const message = ref('')

async function verifyOTP() {
  const res = await fetch('http://localhost:8000/auth/verify-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, otp: otp.value }),
  })

  const data = await res.json()
  if (res.ok) {
    localStorage.setItem('token', data.access_token)
    message.value = 'OTP verified! You are logged in.'
  } else {
    message.value = data.detail || 'Invalid OTP'
  }
}
</script>


<template>
  <div class="max-w-sm mx-auto p-6 bg-white rounded-2xl shadow">
    <h2 class="text-xl font-bold mb-4 text-center">Verify OTP</h2>

    <form @submit.prevent="verifyOTP">
      <div class="mb-3">
        <label class="block text-sm mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded p-2" required />
      </div>

      <div class="mb-3">
        <label class="block text-sm mb-1">OTP</label>
        <input v-model="otp" type="text" class="w-full border rounded p-2" required />
      </div>

      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
      >
        Verify OTP
      </button>
    </form>

    <p v-if="message" class="text-green-600 mt-3 text-center">{{ message }}</p>
  </div>
</template>

