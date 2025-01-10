<template>
  <div class="sports-card">
    <div class="title">
      <p>Leagues</p>
      <Button><i class="pi pi-search" @click="toggleSearch"></i></Button>
    </div>
    <input v-if="isSearching" type="text" v-model="searchQuery" placeholder="Search sports..." />
    <div v-if="isLoaded" class="content">
      <ul>
        <li v-for="sport in filteredSports" :key="sport.id">
          <button @click="handleClick(sport)"><i></i> {{ sport.name }}</button>
        </li>
      </ul>
    </div>
    <div v-else class="empty-content"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const isLoaded = ref<boolean>(true)
const isSearching = ref<boolean>(false)
const sports = ref([
  {
    id: 1,
    name: 'Premier League',
  },
  {
    id: 2,
    name: 'La Liga',
  },
  {
    id: 3,
    name: 'Bundesliga',
  },
  {
    id: 4,
    name: 'Serie A',
  },
  {
    id: 5,
    name: 'Ligue 1',
  },
])

const toggleSearch = (): void => {
  isSearching.value = !isSearching.value
}

const searchQuery = ref<string>('')

const filteredSports = computed(() => {
  return sports.value.filter((sport) =>
    sport.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

const router = useRouter()

const handleClick = (sport: { id: number; name: string }) => {
  router.push({ name: 'Sports', params: { sport: sport.name.toLowerCase() } })
}
</script>

<style scoped>
.sports-card {
  position: fixed;
  margin-left: 3rem;
  width: 15%;
  background-color: var(--color-grey-100);
  border-radius: 15px;
  box-shadow: 0 2px 10px var(--color-grey-450);
  border: 1px solid var(--color-grey-550);
  height: 40rem;
}
.title {
  background-color: var(--color-grey-550);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border: 1px solid var(--color-grey-550);
  box-shadow: 0 2px 10px var(--color-grey-550);
  height: 10%;
  display: flex;
  justify-content: space-between;
}
i {
  margin-right: 10px;
}
.pi.pi-search {
  color: var(--color-primary-gray-light);
  font-weight: 600;
  margin: 15px;
  font-size: 25px;
}
input {
  width: 100%;
  padding: 10px;
}
p {
  color: var(--color-primary-gray-light);
  font-weight: 600;
  margin: 10px;
  font-size: 25px;
}
.content {
  max-height: 100%;
  overflow-y: auto;
}
ul {
  margin: 15px;
  font-size: 25px;
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
li button {
  all: unset;
  cursor: pointer;
  display: flex;
  align-items: center;
  width: 100%;
}
li button:hover {
  color: var(--color-grey-350);
}
</style>
