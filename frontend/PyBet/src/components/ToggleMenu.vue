<template>
  <div>
<<<<<<< HEAD
    <Drawer v-model:visible="visible" header="Menu" class="custom-sidebar w-full md:w-20rem lg:w-30rem">
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus consequuntur quaerat necessitatibus iste ullam repudiandae qui accusantium odio labore vel.</p>
    </Drawer>
    <Button icon="pi pi-bars" @click="visible = true" class="custom-button" :style="{ fontSize: '1.5rem' }"/>
=======
    <Drawer
      v-model:visible="visible"
      header="Menu"
      class="custom-sidebar w-full md:w-20rem lg:w-30rem"
    >
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus consequuntur quaerat
        necessitatibus iste ullam repudiandae qui accusantium odio labore vel.
      </p>
    </Drawer>
    <PrimeButton
      icon="pi pi-bars"
      @click="visible = true"
      class="custom-button"
      :style="{ fontSize: '1.5rem' }"
    />
>>>>>>> origin/main
  </div>
</template>

<script lang="ts" setup>
<<<<<<< HEAD
import Drawer from 'primevue/drawer';
import Button from 'primevue/button';
import { ref } from "vue";

const visible = ref(false);
=======
import Drawer from 'primevue/drawer'
import { ref } from 'vue'

const visible = ref(false)
>>>>>>> origin/main
</script>

<style scoped>
.custom-button {
  color: var(--color-primary-gray-light);
  transition: color 0.3s ease;
}

.custom-button:hover {
  color: var(--color-green-300);
}

.custom-button .pi {
<<<<<<< HEAD
  color: inherit; 
=======
  color: inherit;
>>>>>>> origin/main
  transition: color 0.3s ease;
}

.custom-sidebar .p-drawer-content {
  background-color: aqua;
}
<<<<<<< HEAD
</style>
=======
</style>
>>>>>>> origin/main
