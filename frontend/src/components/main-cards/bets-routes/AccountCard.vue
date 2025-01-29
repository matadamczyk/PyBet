<template>
  <div class="account-container">
    <h3>Account Overview</h3>
    <div class="main-container">
      <div class="balance">
        <p>
          Your PyCoins <br /><span>{{ pyCoins.toFixed(2) }}</span>
        </p>
        <button @click="addPyCoins">Add PyCoins</button>
        <button @click="showHistory = true">Betting History</button>
      </div>
    </div>

    <Dialog v-model:visible="showHistory" modal header="Betting History" :style="{ width: '50vw' }">
      <div class="betting-history">
        <ul>
          <li v-for="bet in bettingHistory" :key="bet.id" class="bet-item">
            <div class="bet-header">{{ bet.matchTeams }}</div>
            <div class="bet-details">
              Pick: {{ bet.selectedOption }} | Odds: {{ bet.selectedOdds.toFixed(2) }}
              <br />
              Stake: {{ bet.stake }} PyCoins | Date: {{ new Date(bet.date).toLocaleDateString() }}
            </div>
          </li>
        </ul>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeMount } from 'vue'
import { usePybetStore } from '../../../stores/store'
import type { BetHistory } from '../../../types/BetHistory.interface'
import Dialog from 'primevue/dialog'

const store = usePybetStore()
const pyCoins = ref(0)
const bettingHistory = ref<BetHistory[]>([])
const showHistory = ref(false)

const fetchBettingHistory = async () => {
  const email = localStorage.getItem('userEmail')
  const response = await fetch(`http://localhost:8000/get_user_picked_options/?email=${email}`)
  if (response.ok) {
    bettingHistory.value = await response.json()
  } else {
    console.error('Failed to fetch betting history')
  }
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
        email: localStorage.getItem('userEmail'),
      }),
      credentials: 'include',
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

watch(
  () => store.pycoins,
  (newValue) => {
    pyCoins.value = newValue
    store.pycoins = pyCoins.value
  },
)

onMounted(async () => {
  await fetchBettingHistory()
})

onBeforeMount(async () => {
  await store.fetchUserPycoins()
})
</script>

<style scoped>
.account-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  text-align: center;
}

.main-container {
  display: flex;
  flex-direction: row;
  align-items: start;
  justify-content: center;
}

.betting-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

h3 {
  font-size: 5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  border: 3px solid var(--color-grey-150);
  border-radius: 15px;
  padding: 1rem;
  background-color: var(--color-grey-150);
}

.balance {
  padding: 1rem;
  border-radius: 15px;
  background-color: var(--color-grey-400);
  margin-right: 1rem;
}

p {
  font-size: 2rem;
  font-weight: 700;
  margin: 1rem;
  color: var(--color-primary-gray-light);
}

span {
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-primary-green);
}

button {
  background-color: var(--color-primary-green);
  font-size: 2rem;
  font-weight: 700;
  border-radius: 15px;
  padding: 1rem;
  margin: 0 1rem 2rem 1rem;
  cursor: pointer;
}

button:hover {
  background-color: var(--color-green-150);
}

h4 {
  font-size: 3rem;
  font-weight: 700;
  border: 3px solid var(--color-grey-150);
  border-radius: 15px;
  padding: 1rem;
  background-color: var(--color-grey-150);
  margin-left: 1rem;
}

ul {
  list-style: none;
  margin-top: 1rem;
  border-radius: 15px;
  padding: 1rem;
  font-size: 1.5rem;
  color: var(--color-primary-gray-light);
}
li {
  border-bottom: 3px solid var(--color-grey-150);
}

.bet-item {
  background-color: var(--color-grey-400);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.bet-header {
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-primary-green);
  margin-bottom: 0.5rem;
}

.bet-details {
  color: var(--color-primary-gray-light);
}

button {
  margin: 0.5rem;
}
</style>
