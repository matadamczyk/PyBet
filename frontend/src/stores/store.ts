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

  const tokens = ref<string>(localStorage.getItem('tokens') || '')

  const setTokens = (newTokens: string) => {
    tokens.value = newTokens
    localStorage.setItem('tokens', newTokens)
  }

  const isLoading = ref<boolean>(false)

  const pycoins = ref<number>(0)

  const updatePycoins = (amount: number) => {
    pycoins.value = amount
  }

  const deductPycoins = (amount: number) => {
    if (pycoins.value >= amount) {
      pycoins.value -= amount
      return true
    }
    return false
  }

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

  const fetchUserPycoins = async () => {
    if (isLogged.value) {
      try {
        const response = await fetch('http://localhost:8000/user-pycoins/', {
          headers: {
            'Authorization': `Bearer ${tokens.value}`,
          },
        })
        if (response.ok) {
          const data = await response.json()
          pycoins.value = data.pycoins
        }
      } catch (error) {
        console.error('Error fetching user pycoins:', error)
      }
    }
  }

  return { isLogged, logout, betEvents, tokens, fetchMatches, matches, isLoading, pycoins, updatePycoins, deductPycoins, fetchUserPycoins, setTokens }
})
