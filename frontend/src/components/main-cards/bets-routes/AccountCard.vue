<template>
  <div class="account-container">
    <h3>Account Overview</h3>
    <div class="balance">
      <p>Your PyCoins: {{ pyCoins }}</p>
      <button @click="addPyCoins">Add PyCoins</button>
    </div>
    <h4>Betting History</h4>
    <ul>
      <li v-for="bet in bettingHistory" :key="bet.id">
        {{ bet.selectedOption }} on {{ bet.date }} - Stake: {{ bet.stake }} PyCoins
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePybetStore } from '../../../stores/store'
import type { BetHistory } from '../../../types/BetHistory.interface'
const store = usePybetStore()
const pyCoins = ref(0)
const bettingHistory = ref<BetHistory[]>([])

const fetchBettingHistory = async () => {
  const response = await fetch('http://localhost:8000/bets/')
  bettingHistory.value = await response.json()
}

const addPyCoins = async () => {
  if (!store.isLogged) {
    alert('Please log in to add PyCoins.')
    return
  }
  
  const amount = prompt('Enter amount of PyCoins to add:')
  if (amount && !isNaN(Number(amount))) {
    const response = await fetch('http://localhost:8000/add-pycoins/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        amount: Number(amount),
        email: localStorage.getItem('userEmail')
      }),
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      store.updatePycoins(data.pycoins)
      alert('PyCoins added successfully!')
    } else {
      alert('Failed to add PyCoins.')
    }
  }
}

watch(() => store.pycoins, (newValue) => {
  pyCoins.value = newValue
  store.pycoins = pyCoins.value
})

onMounted(async () => {
  await fetchBettingHistory()
  await store.fetchUserPycoins()
})
</script>

<style scoped>
.account-container {
  padding: 20px;
  background-color: var(--color-grey-150);
  border-radius: 15px;
  box-shadow: 0 2px 10px var(--color-grey-550);
}
</style>