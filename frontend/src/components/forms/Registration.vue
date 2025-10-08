<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const phone = ref('')
const password = ref('')
const message = ref('')
const otp = ref('')

async function register() {
  message.value = ''
  otp.value = ''
  const res = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, phone: phone.value, password: password.value }),
  })

  const data = await res.json()
  if (res.ok) {
    message.value = data.message
    otp.value = data.otp_demo // remove this in production
  } else {
    message.value = data.detail || 'Registration failed'
  }
}
</script>


<template>
  <div class="max-w-sm mx-auto p-6 bg-white rounded-2xl shadow">
    <h2 class="text-xl font-bold mb-4 text-center">Register</h2>

    <form @submit.prevent="register">
      <div class="mb-3">
        <label class="block text-sm mb-1">Email</label>
        <input v-model="email" type="email" class="w-full border rounded p-2" required />
      </div>

      <div class="mb-3">
        <label class="block text-sm mb-1">Phone (optional)</label>
        <input v-model="phone" type="text" class="w-full border rounded p-2" />
      </div>

      <div class="mb-3">
        <label class="block text-sm mb-1">Password (optional)</label>
        <input v-model="password" type="password" class="w-full border rounded p-2" />
      </div>

      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
      >
        Register
      </button>
    </form>

    <p v-if="message" class="text-green-600 mt-3 text-center">{{ message }}</p>
    <p v-if="otp" class="text-gray-500 mt-1 text-center">Demo OTP: {{ otp }}</p>
  </div>
</template>

