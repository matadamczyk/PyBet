<template>
  <div class="bets-card">
    <div class="title">
      <p>Type of competition</p>
      <div class="line"></div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.bets-card {
  width: 70%;
  margin-right: 5rem;
  background-color: var(--color-grey-450);
  margin: 0 5rem 0 5rem;
  border-radius: 30px;
  box-shadow: 0 2px 10px var(--color-grey-450);
}
.title {
  text-align: center;
}
.line {
  width: 100%;
  height: 1px;
  background: rgb(153, 153, 153);
  background: linear-gradient(
    45deg,
    var(--color-grey-450) 0%,
    var(--color-primary-gray-light) 50%,
    var(--color-grey-450) 100%
  );
}
p {
  font-size: 2rem;
  color: var(--color-primary-gray-light);
  margin: 1rem;
}
</style>