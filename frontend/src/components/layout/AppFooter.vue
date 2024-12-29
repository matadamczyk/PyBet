<template>
  <footer>
    <div class="info">
      <p>&copy; 2024 PyBet. All rights reserved.</p>
      <nav>
        <ul>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Contact Us</a></li>
        </ul>
      </nav>
    </div>
    <div class="repo">
      <a href="http://github.com/matadamczyk/PyBet"
        >Github repository <i class="pi pi-github"></i
      ></a>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
footer {
  margin-top: 5rem;
  margin-right: 5rem;
  margin-bottom: 3rem;
  background-color: var(--color-green-500);
  width: 915px;
  height: 12rem;
  border-radius: 15px;
  border: 2px solid var(--color-green-550);
  box-shadow: 0 0 10px 0 var(--color-green-550);
  color: var(--color-primary-gray-light);
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}
.repo {
  font-size: 30px;
}
i:hover,
a:hover {
  color: var(--color-grey-200);
}
</style>
