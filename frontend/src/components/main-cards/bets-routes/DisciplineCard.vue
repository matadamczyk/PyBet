<template>
  <div class="discipline-card">
    <div class="league-buttons">
      <div v-for="league in leagues" :key="league" @click="(event) => handleClick(event, league)" :class="{ active: selectedLeague === league }">
        {{ league }}
      </div>
    </div>
    <LeagueCard :selectedLeague="selectedLeague" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { usePybetStore } from '@/stores/store';
import LeagueCard from './LeagueCard.vue';

const route = useRoute();
const store = usePybetStore();

const selectedLeague = ref('');

const leagues = computed(() => {
  const leagueSet = new Set(store.events.map(event => event.league));
  return Array.from(leagueSet);
});

const filteredEvents = computed(() => {
  if (!selectedLeague.value) return [];
  return store.events.filter(event => event.league === selectedLeague.value);
});

const handleClick = (event: MouseEvent, league: string) => {
  selectedLeague.value = league;
}
</script>

<style scoped>
.discipline-card {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  
}

.league-buttons {
  display: flex;
  gap: 1rem;
  display: flex;
  flex-direction: row;
  position: fixed;
  top: 20%;
  margin-bottom: 5rem;
}

.league-buttons div {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  cursor: pointer;
  border: 2px solid var(--color-grey-250);
  border-radius: 15px;
  background-color: var(--color-grey-150);
  box-shadow: 0 0 20px 0 var(--color-grey-150);
}

.league-buttons div.active {
  background-color: #f4f4f4;
  font-weight: bold;
}

</style>