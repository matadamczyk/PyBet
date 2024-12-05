<template>
  <div class="sports-container">
    <SportsCard />
    <BetsCard />
  </div>
</template>

<script setup lang="ts">
import SportsCard from './main-cards/SportsCard.vue'
import BetsCard from './main-cards/BetsCard.vue'
</script>

<style scoped>
.sports-container {
  display: flex;
  flex-direction: row;
  margin-top: 12%;
  width: 100%;
  height: 40rem;
}
</style>