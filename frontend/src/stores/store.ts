import type { Bet } from '@/types/Bet.interface'
import type Match from '../types/Match.interface'
import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePybetStore = defineStore('pybet', () => {
  const isLogged = ref<boolean>(localStorage.getItem('isLogged') === 'true')

  const logout = () => {
    isLogged.value = false
    localStorage.setItem('isLogged', 'false')
  }

  const matches = ref<Match[]>([])

  const betEvents = ref<Bet[]>([])

  const tokens = ref<number>(0.0)

  const isLoading = ref<boolean>(false)

  const fetchMatches = async () => {
    isLoading.value = true
    try {
      const response = await axios.get('http://localhost:8000/matches')
      console.log('Fetched matches:', response.data)
      matches.value = response.data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Error fetching matches:', error.response?.status, error.response?.data)
      } else {
        console.error('Unexpected error:', error)
      }
    } finally {
      isLoading.value = false
    }
  }

  return { isLogged, logout, betEvents, tokens, fetchMatches, matches, isLoading }
})
