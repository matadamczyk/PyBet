<template>
  <div>
    <div v-if="filteredEvents.length">
      <div v-for="event in filteredEvents" :key="event.date" class="event-row">
        <div class="team">{{ event.homeTeam }}</div>
        <p>vs</p>
        <div class="team">{{ event.awayTeam }}</div>
        <div>{{ event.date }}</div>
        <button :class="{ active: selection[event.date] === event.homeTeam }" class="odds" @click="handleSelect(event.date, event.homeTeam)">{{ event.odds.homeWin }}
          <h6>{{ event.homeTeam }}</h6>
        </button>
        <button :class="{ active: selection[event.date] === 'Draw' }" class="odds" @click="handleSelect(event.date, 'Draw')">{{ event.odds.draw }}
          <h6>Draw</h6>
        </button>
        <button :class="{ active: selection[event.date] === event.awayTeam }" class="odds" @click="handleSelect(event.date, event.awayTeam)">
          {{ event.odds.awayWin }}
          <h6>{{ event.awayTeam }}</h6>
        </button>
        <div>
          <button @click="placeBet(event)"><i class="pi pi-plus"></i></button>
        </div>
      </div>
    </div>
    <div v-else>No league selected.</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps } from 'vue'
import { usePybetStore } from '@/stores/store'

const props = defineProps<{ selectedLeague: string }>()
const store = usePybetStore()

const filteredEvents = computed(() => {
  return store.events.filter((event) => event.league === props.selectedLeague)
})

const selection = ref<{ [key: string]: string }>({});

const handleSelect = (date: string, team: string) => {
  if (selection.value[date] === team) {
    delete selection.value[date];
  } else {
    selection.value[date] = team;
  }
}

const placeBet = (event: any) => {
  const selectedOption = selection.value[event.date];
  if (selectedOption) {
    store.betEvents.push({
      ...event,
      selectedOption,
      selectedOdds: event.odds[selectedOption === 'Draw' ? 'draw' : selectedOption === event.homeTeam ? 'homeWin' : 'awayWin']
    });
  }
}

</script>

<style scoped>
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
div, button {
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
</style>