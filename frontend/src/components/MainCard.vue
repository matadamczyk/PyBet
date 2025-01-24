<template>
  <div class="sports-container">
    <SportsCard />
    <BetsCard :matches="matches" />
    <CouponCard />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import SportsCard from './main-cards/SportsCard.vue'
import BetsCard from './main-cards/BetsCard.vue'
import CouponCard from './main-cards/CouponCard.vue'

const props = defineProps({
  matches: Array,
})
</script>

<style scoped>
.sports-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 10%;
  width: 100%;
  height: 40rem;
}
</style>
