import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/components/main-cards/bets-routes/HomeCard.vue'),
  },
  {
    path: '/sports/:sport',
    name: 'Sports',
    component: () => import('@/components/main-cards/bets-routes/DisciplineCard.vue'),
    children: [
      {
        path: 'league/:league',
        name: 'League',
        component: () => import('@/components/main-cards/bets-routes/LeagueCard.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
