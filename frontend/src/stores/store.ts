import { computed, ref } from 'vue'

import { defineStore } from 'pinia'

export const usePybetStore = defineStore('pybet', () => {
  const isLogged = ref<boolean>(false)

  const logout = () => {
    isLogged.value = false
  }

  const events = ref([
    {
      league: 'Premier League',
      homeTeam: 'Manchester United',
      awayTeam: 'Chelsea',
      date: '2023-11-01',
      odds: {
        homeWin: 1.8,
        draw: 3.5,
        awayWin: 4.0,
      },
    },
    {
      league: 'Premier League',
      homeTeam: 'Liverpool',
      awayTeam: 'Arsenal',
      date: '2023-11-04',
      odds: {
        homeWin: 2.0,
        draw: 3.4,
        awayWin: 3.8,
      },
    },
    {
      league: 'Premier League',
      homeTeam: 'Tottenham',
      awayTeam: 'Manchester City',
      date: '2023-11-05',
      odds: {
        homeWin: 3.0,
        draw: 3.3,
        awayWin: 2.2,
      },
    },
    {
      league: 'La Liga',
      homeTeam: 'Real Madrid',
      awayTeam: 'Barcelona',
      date: '2023-11-02',
      odds: {
        homeWin: 2.1,
        draw: 3.2,
        awayWin: 3.6,
      },
    },
    {
      league: 'La Liga',
      homeTeam: 'Atletico Madrid',
      awayTeam: 'Sevilla',
      date: '2023-11-06',
      odds: {
        homeWin: 1.9,
        draw: 3.5,
        awayWin: 4.1,
      },
    },
    {
      league: 'La Liga',
      homeTeam: 'Valencia',
      awayTeam: 'Villarreal',
      date: '2023-11-07',
      odds: {
        homeWin: 2.4,
        draw: 3.1,
        awayWin: 3.2,
      },
    },
    {
      league: 'Serie A',
      homeTeam: 'Juventus',
      awayTeam: 'AC Milan',
      date: '2023-11-03',
      odds: {
        homeWin: 2.5,
        draw: 3.0,
        awayWin: 3.0,
      },
    },
    {
      league: 'Serie A',
      homeTeam: 'Inter Milan',
      awayTeam: 'Napoli',
      date: '2023-11-08',
      odds: {
        homeWin: 2.3,
        draw: 3.3,
        awayWin: 3.4,
      },
    },
    {
      league: 'Serie A',
      homeTeam: 'Roma',
      awayTeam: 'Lazio',
      date: '2023-11-09',
      odds: {
        homeWin: 2.6,
        draw: 3.0,
        awayWin: 3.1,
      },
    },
  ])

  const betEvents = ref<any[]>([])

  const tokens = ref<number>(0.0);

  return { isLogged, logout, events, betEvents }
})
