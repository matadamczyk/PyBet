<template>
  <nav>
    <div class="flex space-x-8 ml-5">
      <ToggleMenu />
      <a class="normal" href="">Bets</a>
      <a class="normal" href="">Live<i class="fa fa-signal-stream"></i></a>
    </div>
    <div class="h-full object-contain flex space-x-8 ml-5 items-center">
      <img src="@/assets/logo.png" alt="logo" class="h-full object-contain" />
      <span class="logo-label">PyBet</span>
    </div>
    <div class="flex space-x-8 mr-5 items-center">
      <button class="register" @click="showRegisterDialog"><span>Sign up</span></button>
      <button class="normal" @click="showSignInDialog">Sign in</button>
    </div>
    <SignIn
      :visible="signInVisible"
      @update:visible="signInVisible = $event"
      @close="signInVisible = false"
    />
    <RegisterAccount
      :visible="registerVisible"
      @update:visible="registerVisible = $event"
      @close="registerVisible = false"
    />
  </nav>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import ToggleMenu from '../ToggleMenu.vue'
import SignIn from '../account/SignIn.vue'
import RegisterAccount from '../account/RegisterAccount.vue'

const signInVisible = ref(false)
const registerVisible = ref(false)

const showSignInDialog = () => {
  signInVisible.value = true
}

const showRegisterDialog = () => {
  registerVisible.value = true
}
</script>

<style scoped>
nav {
  width: 100%;
}
</style>

<style scoped>
nav {
  width: 100%;
  height: 15%;
  background-color: var(--color-grey-550);
  color: var(--color-primary-gray-light);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  font-size: 1.5rem;
  font-weight: 600;
  box-shadow: 0 2px 10px var(--color-grey-550);
}

body {
  margin: 0;
  padding: 0;
}

img {
  height: 100%;
  object-fit: contain;
}

a {
  position: relative;
  text-decoration: none;
  color: inherit;
  display: inline-block;
}

.normal {
  position: relative;
  display: inline-block;
}

.normal:hover {
  color: var(--color-green-300);
}

.normal::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 4px;
  border-radius: 4px;
  background-color: var(--color-green-300);
  bottom: 0;
  left: 0;
  transform-origin: right;
  transform: scaleX(0);
  transition: transform 0.3s ease-in-out;
}

.normal:hover::before {
  transform-origin: left;
  transform: scaleX(1);
}

.normal:hover::before {
  transform-origin: left;
  transform: scaleX(1);
}

.register {
  background: linear-gradient(var(--color-green-300) 0 0) calc(100% - var(--p, 0%)) / var(--p, 0%)
    no-repeat;
  background-color: var(--color-primary-gray-light);
  color: var(--color-grey-550);
  border-radius: 15px;
  padding: 5px 10px;
  display: inline-block;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition:
    0.4s,
    background-position 0s;
}

.register:hover {
  --p: 100%;
}

.register span {
  position: relative;
  z-index: 1;
}
.logo-label {
  font-style: italic;
  font-weight: 700;
  font-size: 4rem;
  color: #fff;
}
</style>