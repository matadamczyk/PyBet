<template>
  <div class="home-card">
    <div class="welcome-message">
      <h1>Welcome to Py<span class="green">Bet</span></h1>
      <h2>Your ultimate sports <span class="green">bet</span>ting platform</h2>
      <div class="description">
        <p>
          At PyBet, we offer the best odds and a wide range of sports events to bet on. <br />
          Whether you're a fan of football, basketball, tennis, or any other sport, we've got you
          covered.
        </p>
        <p>
          Join us today and start placing your bets on your favorite teams and players. <br />
          Experience the thrill of sports betting with PyBet!
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.home-card {
  display: flex;
  flex-direction: column;
}
.welcome-message {
  text-align: center;
}
h1 {
  font-weight: 700;
  font-size: 5rem;
  color: var(--color-grey-500);
}
h2 {
  font-size: 3rem;
  margin-bottom: 40px;
}
.green {
  color: var(--color-primary-green);
}
p {
  font-size: 1.5rem;
}
.description {
  border: 2px solid var(--color-grey-200);
  border-radius: 15px;
  padding: 20px;
  background-color: var(--color-grey-150);
  box-shadow: 0 0 15px 0 var(--color-grey-200);
}

@media (min-aspect-ratio: 2560/1600) {
  .home-card {
    scale: 0.8;
  }
}
</style>
