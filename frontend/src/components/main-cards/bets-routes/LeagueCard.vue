<template>
  <div>
    <div v-if="store.isLoading" class="loader">Loading matches...</div>
    <div v-else-if="store.matches.length">
      <div v-for="match in store.matches" :key="match.identifier" class="event-row">
        <div class="team">{{ match.team1 }}</div>
        <p>vs</p>
        <div class="team">{{ match.team2 }}</div>
        <button
          :class="{ active: selection[match.identifier] === match.team1 }"
          class="odds"
          @click="handleSelect(match.identifier, match.team1)"
        >
          {{ match.course1 }}
          <h6>{{ match.team1 }}</h6>
        </button>
        <button
          :class="{ active: selection[match.identifier] === 'Draw' }"
          class="odds"
          @click="handleSelect(match.identifier, 'Draw')"
        >
          {{ match.courseX }}
          <h6>Draw</h6>
        </button>
        <button
          :class="{ active: selection[match.identifier] === match.team2 }"
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

defineProps<{ selectedLeague: string }>()
const store = usePybetStore()

const selection = ref<{ [key: string]: string }>({})

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
        (selectedOption === 'Draw'
          ? parseFloat(match.courseX)
          : selectedOption === match.team1
          ? parseFloat(match.course1)
          : parseFloat(match.course2)),
    }

    store.betEvents.push(bet)
  }
}

onBeforeMount(async () => {
  await store.fetchMatches()
})
</script>

<style scoped>
.loader {
  font-size: 20px;
  text-align: center;
  margin: 20px;
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
</style>
