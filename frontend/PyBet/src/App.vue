<template>
  <div>
    <AppNavbar />
    <MainCard />
  </div>
</template>

<script setup>
import AppNavbar from './components/layout/AppNavbar.vue'
import MainCard from './components/MainCard.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&family=Teko:wght@300..700&display=swap');

:root {
  --color-primary-gray-light: #cccccc;
  --color-primary-gray-medium-light: #999999;
  --color-primary-gray-medium: #666666;
  --color-primary-gray-dark: #333333;
  --color-primary-green: #98e827;

  --color-grey-100: #c4c4c4;
  --color-grey-150: #b2b2b2;
  --color-grey-200: #a0a0a0;
  --color-grey-250: #8e8e8e;
  --color-grey-300: #7c7c7c;
  --color-grey-350: #6b6b6b;
  --color-grey-400: #595959;
  --color-grey-450: #474747;
  --color-grey-500: #353535;
  --color-grey-550: #232323;

  --color-green-100: #ccf394;
  --color-green-150: #bdf074;
  --color-green-200: #adec54;
  --color-green-250: #9ee934;
  --color-green-300: #8ee118;
  --color-green-350: #79c114;
  --color-green-400: #65a111;
  --color-green-450: #51810d;
  --color-green-500: #3c600a;
  --color-green-550: #284006;
}

body {
  font-family: 'Roboto Condensed', sans-serif;
  background-color: var(--color-primary-gray-light);
  color: var(--color-primary-gray-dark);
}

h1 {
  color: var(--color-primary-green);
}
/* TODO: poprawic css dla sidebara */
.p-drawer-header {
  background-color: var(--color-grey-550);
  border-right: 1px solid var(--color-primary-gray-light);
  color: var(--color-primary-gray-light);
}
.p-drawer-content {
  height: 100%;
  background-color: var(--color-grey-550);
  border-right: 1px solid var(--color-primary-gray-light);
  color: var(--color-primary-gray-light);
}
.p-dialog-mask {
  background-color: rgba(0, 0, 0, 0.6) !important;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}
.p-dialog {
  border-radius: 20px !important;
  box-shadow:var(--p-dialog-shadow);
  background: var(--color-grey-500) !important;  
}
.p-drawer-header {
  padding: 10px !important;
}
.p-button-text.p-button-secondary {
  color: var(--color-primary-gray-medium-light) !important;
  margin: 10px;
}
</style>