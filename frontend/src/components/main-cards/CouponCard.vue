<template>
  <div class="coupon-container">
    <div class="label">
      <h3>Coupon</h3>
    </div>
    <div v-if="isEmpty" class="empty-coupon">
      <i class="pi pi-star"></i>
      <h4>Coupon is waiting for your first bet.</h4>
    </div>
    <div class="submit">
      <div class="info-row">
        <div class="info">
          <p class="title">DEPOSIT</p>
          <i class="pi pi-wallet"></i>
        </div>
        <div class="info">
          <p class="title">ODDS</p>
          <p class="value">{{ odds.toFixed(2) }}</p>
        </div>
        <div class="info">
          <p class="title">RATE</p>
          <p class="value">{{ rate.toFixed(2) }}</p>
        </div>
      </div>
      <Button>PLACE A BET</Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isEmpty = ref<boolean>(true);
const odds = ref<number>(0.0);
const rate = ref<number>(50.0);
</script>

<style scoped>
.coupon-container {
  background-color: var(--color-grey-150);
  border-radius: 15px;
  border: 1px solid var(--color-grey-550);
  box-shadow: 0 2px 10px var(--color-grey-550);
  width: 20%;
}
.label {
  background-color: var(--color-grey-550);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border: 1px solid var(--color-grey-550);
  box-shadow: 0 2px 10px var(--color-grey-550);
  height: 10%;
}
.empty-coupon {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60%;
  text-align: center;
  padding: 10px;
}
h3 {
  color: var(--color-primary-gray-light);
  font-weight: 600;
  margin: 10px;
  font-size: 25px;
}
.pi.pi-star {
  font-size: 50px;
  margin-bottom: 10px;
}
.pi.pi-wallet {
  font-size: 40px;
}
h4 {
  color: var(--color-grey-550);
  font-size: 30px;
  font-weight: 500;
}
.submit {
  background-color: var(--color-grey-100);
  height: 30%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 0 2px 10px var(--color-grey-550);
}
.info-row {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.info {
  background-color: var(--color-grey-150);
  height: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 10px;
  width: 100px;
  height: 80px;
  border-radius: 15px;
}
Button {
  margin-top: 10px;
  background-color: var(--color-primary-green);
  width: 340px;
  height: 50px;
  border-radius: 15px;
  font-size: 25px;
  font-weight: 600;
}
Button:hover {
  background-color: var(--color-green-100);
}
.value {
  font-size: 30px;
  font-weight: 700;
}
</style>