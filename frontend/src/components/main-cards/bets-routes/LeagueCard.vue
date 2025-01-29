<template>
  <div class="league-container">
    <div v-if="store.isLoading" class="loader">
      <div class="spinner"></div>
      <p class="loading-text">
        Loading matches<span class="dot">.</span><span class="dot">.</span
        ><span class="dot">.</span>
      </p>
    </div>
    <div v-else-if="store.matches.length" class="matches-container">
      <div class="legend">
        <span class="profitable-legend">Profitable Odds</span>
      </div>
      <div v-for="match in store.matches" :key="match.identifier" class="event-row">
        <div class="team">{{ match.team1 }}</div>
        <p>vs</p>
        <div class="team">{{ match.team2 }}</div>
        <button
          :class="{
            active: selection[match.identifier] === match.team1,
            profitable: isProfitableOdd(match.identifier, '1'),
          }"
          class="odds"
          @click="handleSelect(match.identifier, match.team1)"
        >
          {{ match.course1 }}
          <h6>{{ match.team1 }}</h6>
        </button>
        <button
          :class="{
            active: selection[match.identifier] === 'Draw',
            profitable: isProfitableOdd(match.identifier, 'X'),
          }"
          class="odds"
          @click="handleSelect(match.identifier, 'Draw')"
        >
          {{ match.courseX }}
          <h6>Draw</h6>
        </button>
        <button
          :class="{
            active: selection[match.identifier] === match.team2,
            profitable: isProfitableOdd(match.identifier, '2'),
          }"
          class="odds"
          @click="handleSelect(match.identifier, match.team2)"
        >
          {{ match.course2 }}
          <h6>{{ match.team2 }}</h6>
        </button>
        <div>
          <button @click="placeBet(match)"><i class="pi pi-plus"></i></button>
        </div>
      </div>
    </div>
    <div v-else>No matches available.</div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onBeforeMount } from 'vue'
import { usePybetStore } from '../../../stores/store'
import type { Bet } from '../../../types/Bet.interface'

interface OddsData {
  id: string;
  outcome: string;
}

defineProps<{ selectedLeague: string }>()
const store = usePybetStore()

const selection = ref<{ [key: string]: string }>({})
const oddsData = ref<OddsData[]>([])

const fetchOddsData = async () => {
  try {
    const response = await fetch('http://localhost:8000/profitable/')
    if (!response.ok) {
      throw new Error('Failed to fetch odds data')
    }
    oddsData.value = await response.json()
  } catch (error) {
    console.error('Error fetching odds data:', error)
  }
}

const isProfitableOdd = (matchId: string, type: string) => {
  const profitableMatch = oddsData.value.find((match) => match.id === matchId)
  if (profitableMatch) {
    return profitableMatch.outcome === type
  }
  return false
}

const handleSelect = (date: string, team: string) => {
  if (selection.value[date] === team) {
    delete selection.value[date]
  } else {
    selection.value[date] = team
  }
}

const placeBet = (match: {
  identifier: string
  team1: string
  team2: string
  course1: string
  courseX: string
  course2: string
}) => {
  const selectedOption = selection.value[match.identifier]
  if (selectedOption) {
    const bet: Bet = {
      homeTeam: match.team1,
      awayTeam: match.team2,
      date: new Date().toISOString(),
      selectedOption,
      selectedOdds:
        selectedOption === 'Draw'
          ? parseFloat(match.courseX)
          : selectedOption === match.team1
            ? parseFloat(match.course1)
            : parseFloat(match.course2),
    }

    store.betEvents.push(bet)
  }
}

onBeforeMount(async () => {
  await store.fetchMatches()
  await fetchOddsData()
})
</script>

<style scoped>
.league-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.matches-container {
  margin-top: 275%;
}
.loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
}
.spinner {
  border: 20px solid var(--color-grey-200);
  border-top: 20px solid var(--color-primary-green);
  border-radius: 50%;
  width: 100px;
  height: 100px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  70% {
    transform: rotate(320deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.dot {
  display: inline-block;
  margin: 0 2px;
  border-radius: 50%;
  animation: pulse 0.6s infinite alternate;
}
.dot:nth-child(2) {
  animation-delay: 0.2s;
}
.dot:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes pulse {
  0% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
.loading-text {
  font-size: 70px;
  font-weight: 500;
}
.event-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 20px;
  padding: 15px;
  border-radius: 15px;
  background-color: var(--color-grey-150);
  gap: 20px;
}
div,
button {
  font-size: 20px;
}
.team {
  font-weight: 600;
  font-size: 25px;
}
.odds {
  background-color: var(--color-grey-100);
  border-radius: 15px;
  margin: 10px;
  padding: 10px;
}
.odds:hover {
  background-color: var(--color-grey-200);
}
.active {
  background-color: var(--color-grey-200);
}
h6 {
  opacity: 0.7;
  font-size: 15px;
}

.event-row:first-child {
  margin-top: 10%;
}

.profitable {
  border: 3px solid var(--color-primary-green);
}

.legend {
  margin: 20px 0;
  font-size: 25px;
  font-weight: 500;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profitable-legend {
  border: 3px solid var(--color-primary-green);
  padding: 5px 10px;
  border-radius: 5px;
  background-color: var(--color-grey-200);
  color: var(--color-primary-green);
}
</style>
