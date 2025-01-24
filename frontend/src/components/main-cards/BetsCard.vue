<template>
  <div class="bets-card">
    <div v-if="route.path === '/sports'" class="hint-card">
      <h1>To start betting choose one of the sports in the table</h1>
      <div class="pointer">
        <i class="pi pi-angle-left first" :class="iconColor1"></i>
        <i class="pi pi-angle-left second" :class="iconColor2"></i>
        <i class="pi pi-angle-left third" :class="iconColor3"></i>
      </div>
    </div>
    <router-view v-else />
    <!-- <AppFooter /> -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, defineProps } from 'vue'
import { useRoute } from 'vue-router'
import AppFooter from '../layout/AppFooter.vue'

const props = defineProps({
  matches: Array,
})

const route = useRoute()

const iconColor1 = ref<string>('color1')
const iconColor2 = ref<string>('color2')
const iconColor3 = ref<string>('color1')

onMounted(() => {
  const interval = setInterval(() => {
    iconColor1.value = iconColor1.value === 'color1' ? 'color2' : 'color1'
    iconColor2.value = iconColor2.value === 'color2' ? 'color1' : 'color2'
    iconColor3.value = iconColor3.value === 'color1' ? 'color2' : 'color1'
  }, 1000)

  onUnmounted(() => {
    clearInterval(interval)
  })
})
</script>

<style scoped>
.bets-card {
  width: 100%;
  margin-right: 5rem;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  overflow-y: auto;
}
.hint-card {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-bottom: 50px;
}
h1 {
  font-weight: 700;
  font-size: 3rem;
  color: var(--color-grey-500);
  margin: 2rem;
}
i {
  margin: 2rem -20px;
  font-size: 7rem;
}
.color1 {
  color: var(--color-primary-green);
}
.color2 {
  color: var(--color-primary-red);
}
</style>
