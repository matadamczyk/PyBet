<template>
  <div class="bets-card">
    <router-view />
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppFooter from '../layout/AppFooter.vue';

const route = useRoute()

</script>

<style scoped>
  .bets-card {
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    overflow-y: auto;
  }
</style>
