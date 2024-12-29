<template>
  <div class="discipline-card">
    <h1>Result for {{ route. }}</h1>
    
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<style scoped>

</style>