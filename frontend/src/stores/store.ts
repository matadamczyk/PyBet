import type { Bet } from '@/types/Bet.interface'
import type Match from '../types/Match.interface'
import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePybetStore = defineStore('pybet', () => {
  const isLogged = ref<boolean>(false)

  const logout = () => {
    isLogged.value = false
  }

  const matches = ref<Match[]>([])

  const betEvents = ref<Bet[]>([])

  const tokens = ref<number>(0.0)

  const fetchMatches = async () => {
    try {
      const response = await axios.get('/matches')
      matches.value = response.data
    } catch (error) {
      console.error('Error fetching matches:', error)
    }
  }

  return { isLogged, logout, betEvents, tokens, fetchMatches, matches }
})
