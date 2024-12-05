<template>
  <Dialog
    :visible="visible"
    @update:visible="updateVisible"
    modal
    class="custom-dialog"
    @hide="closeDialog"
  >
    <div class="custom-bg px-6 py-6 md:px-8 lg:px-10">
      <div class="text-center mb-8">
        <img class="w-20 h-auto mx-auto" src="@/assets/logo.png" alt="logo" />

        <div class="custom-title text-3xl font-medium mb-4">Join Us</div>
        <span class="custom-subtitle font-medium leading-normal">Already have an account?</span>
        <a class="custom-link font-medium no-underline ml-2 cursor-pointer">Sign in</a>
      </div>

      <div>
        <label for="email1" class="custom-label font-medium mb-2 block">Email</label>
        <InputText id="email1" type="text" placeholder="Email address" class="w-full mb-4" />

        <label for="password1" class="custom-label font-medium mb-2 block">Password</label>
        <InputText id="password1" type="password" placeholder="Password" class="w-full mb-4" />

        <label for="confirmPassword1" class="custom-label font-medium mb-2 block"
          >Confirm Password</label
        >
        <InputText
          id="confirmPassword1"
          type="password"
          placeholder="Confirm Password"
          class="w-full mb-4"
        />

        <Button label="Register" icon="pi pi-user" class="w-full" />
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

const props = defineProps({
  visible: Boolean,
})

const emits = defineEmits(['close', 'update:visible'])

const checked1 = ref(true)

function closeDialog() {
  emits('close')
}

const updateVisible = (value: boolean) => {
  emits('update:visible', value)
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