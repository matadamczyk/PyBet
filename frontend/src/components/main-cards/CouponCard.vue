<template>
  <div class="coupon-container">
    <div class="label">
      <h3>Coupon</h3>
    </div>
    <div v-if="store.betEvents.length === 0" class="empty-coupon">
      <i class="pi pi-star"></i>
      <h4>Coupon is waiting for your first bet.</h4>
    </div>
    <div v-else class="coupon">
      <ul>
        <li v-for="bet in store.betEvents" :key="bet.date">
          {{ bet.homeTeam }} vs {{ bet.awayTeam }} - {{ bet.date }} <br />
          Selected: {{ bet.selectedOption }} - Odds: {{ bet.selectedOdds }}
          <i class="pi pi-times" @click="removeEvent(bet)"></i>
        </li>
      </ul>
    </div>
    <div class="submit">
      <div class="info-row">
        <button class="info" @click="handleDeposit">
          <p class="title">DEPOSIT</p>
          <i class="pi pi-wallet"></i>
        </button>
        <button class="info">
          <p class="title">ODDS</p>
          <p class="value">
            {{ store.betEvents.length !== 0 ? odds.toFixed(2) : defaultOdd.toFixed(2) }}
          </p>
        </button>
        <button class="info" @click="handleRate">
          <p class="title">RATE</p>
          <p class="value">{{ rate.toFixed(2) }}</p>
        </button>
      </div>
      <Button v-if="store.betEvents.length === 0" class="submit-button" @click="placeBet">
        PLACE A BET
      </Button>
      <Button v-else class="submit-button" @click="placeBet">
        <p class="to-win">Play and win:</p>
        {{ totalPrize.toFixed(2) }}
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePybetStore } from '../../stores/store'
import type { Bet } from '../../types/Bet.interface'

// const isEmpty = ref<boolean>(true)
const defaultOdd = ref<number>(0.0)

const odds = computed(() => {
  return store.betEvents.reduce((total, bet) => total * bet.selectedOdds, 1)
})
const rate = ref<number>(50.0)

const totalPrize = computed(() => {
  return odds.value * rate.value
})

const store = usePybetStore()

const handleDeposit = () => {
  if (!store.isLogged) {
    alert('Please log in to view deposit.')
    return
  }
}

const handleRate = () => {
  if (!store.isLogged) {
    alert('Please log in to change rate.')
    return
  }
  
  const newRate = prompt('Enter new rate:')
  if (newRate && !isNaN(Number(newRate))) {
    const newRateNum = Number(newRate)
    if (newRateNum <= 0) {
      alert('Rate must be greater than 0.')
      return
    }
    if (newRateNum > store.pycoins) {
      alert('Rate cannot be greater than your PyCoins balance.')
      return
    }
    rate.value = newRateNum
  }
}

const placeBet = async () => {
  if (!store.isLogged) {
    alert('Please log in to place a bet.')
    return
  } 
  if (store.betEvents.length === 0) {
    alert('Choose sport events to place a bet.')
    return
  }
  if (!store.deductPycoins(rate.value)) {
    alert('Insufficient PyCoins balance.')
    return
  }

  const betData = {
    selectedOption: store.betEvents.map(bet => bet.selectedOption).join(', '),
    date: new Date().toISOString().split('T')[0],
    selectedOdds: odds.value,
    stake: rate.value,
  }

  const response = await fetch('http://localhost:8000/bets/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${store.tokens}`,
    },
    body: JSON.stringify(betData),
  })

  if (response.ok) {
    alert('Bet successfully placed!')
    store.betEvents = []
  } else {
    alert('Failed to place bet.')
    store.updatePycoins(store.pycoins + rate.value)
  }
}

const removeEvent = (bet: Bet) => {
  const index = store.betEvents.indexOf(bet)
  if (index > -1) {
    store.betEvents.splice(index, 1)
  }
}
</script>

<style scoped>
.coupon-container {
  position: fixed;
  right: 0;
  margin-right: 3rem;
  background-color: var(--color-grey-150);
  border-radius: 15px;
  border: 1px solid var(--color-grey-550);
  box-shadow: 0 2px 10px var(--color-grey-550);
  width: 20%;
  height: 40rem;
}
.label {
  background-color: var(--color-grey-550);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border: 1px solid var(--color-grey-550);
  box-shadow: 0 2px 10px var(--color-grey-550);
  height: 10%;
}
.empty-coupon,
.coupon {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60%;
  text-align: center;
  padding: 10px;
}
h3 {
  color: var(--color-primary-gray-light);
  font-weight: 600;
  margin: 10px;
  font-size: 25px;
}
.pi.pi-star {
  font-size: 50px;
  margin-bottom: 10px;
}
.pi.pi-wallet {
  font-size: 40px;
}
h4 {
  color: var(--color-grey-550);
  font-size: 30px;
  font-weight: 500;
}
.submit {
  background-color: var(--color-grey-100);
  height: 30%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
}
.info-row {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.info {
  background-color: var(--color-grey-150);
  height: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 10px;
  width: 100px;
  height: 80px;
  border-radius: 15px;
}
.info:hover {
  background-color: var(--color-grey-200);
}
.submit-button {
  margin-top: 10px;
  background-color: var(--color-primary-green);
  width: 340px;
  height: 60px;
  border-radius: 15px;
  font-size: 25px;
  font-weight: 600;
}
.submit-button:hover {
  background-color: var(--color-green-100);
}
.value {
  font-size: 30px;
  font-weight: 700;
}
ul {
  overflow-y: auto;
}
li {
  position: relative;
  padding-bottom: 10px;
  margin: 10px 0;
}
li::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 2px;
  background: var(--color-grey-450);
  border-radius: 20%;
}
.pi.pi-times {
  cursor: pointer;
  border: 2px solid var(--color-grey-450);
  border-radius: 15px;
  padding: 5px;
}
.pi.pi-times:hover {
  background-color: var(--color-grey-250);
}
.to-win {
  font-weight: 500;
  font-size: 15px;
}
</style>
