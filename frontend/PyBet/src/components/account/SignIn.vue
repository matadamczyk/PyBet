<template>
  <Dialog :visible="visible" @update:visible="updateVisible" modal class="custom-dialog" @hide="closeDialog">
      <div class="custom-bg p-6 shadow rounded-border w-full mx-auto">
        <div class="text-center mb-8">
          <img class="w-20 h-auto mx-auto" src="@/assets/logo.png" alt="logo">

          <div class="custom-title text-3xl font-medium mb-4">Welcome Back</div>
          <span class="custom-subtitle font-medium leading-normal">Don't have an account?</span>
          <a class="custom-link font-medium no-underline ml-2 cursor-pointer">Create today!</a>
        </div>

        <div>
          <label for="email1" class="custom-label font-medium mb-2 block">Email</label>
          <InputText id="email1" type="text" placeholder="Email address" class="w-full mb-4" />

          <label for="password1" class="custom-label font-medium mb-2 block">Password</label>
          <InputText id="password1" type="password" placeholder="Password" class="w-full mb-4" />

          <div class="flex items-center justify-between mb-12">
            <div class="flex items-center">
              <Checkbox id="rememberme1" v-model="checked1" :binary="true" class="mr-2" />
              <label for="rememberme1">Remember me</label>
            </div>
            <a class="custom-link font-medium no-underline ml-2 text-right cursor-pointer">Forgot password?</a>
          </div>

          <Button label="Sign In" icon="pi pi-user" class="w-full" />
        </div>
      </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';

const props = defineProps({
  visible: Boolean
});

const emits = defineEmits(['close', 'update:visible']);

const checked1 = ref(true);

function closeDialog() {
  emits('close');
}

const updateVisible = (value: boolean) => {
  emits('update:visible', value);
}
</script>

<style scoped>
.custom-dialog {
  width: 83.333333%;
  border-radius: 10px;
}
@media (min-width: 768px) {
  .custom-dialog {
    width: 66.666667%;
  }
}
@media (min-width: 1024px) {
  .custom-dialog {
    width: 33.333333%;
  }
}
img {
  filter: grayscale(100%);
}
.custom-title {
  color: var(--color-primary-gray-light);
}
.custom-subtitle {
  color: var(--color-primary-gray-medium-light);
}
.custom-link {
  color: var(--color-primary-green);
}
.custom-label {
  color: var(--color-primary-gray-light);
}
</style>