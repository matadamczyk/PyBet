export interface Bet {
  homeTeam: string
  awayTeam: string
  date: string
  selectedOption: string
  selectedOdds: number
  odds?: {
    homeWin: number
    draw: number
    awayWin: number
  }
}
