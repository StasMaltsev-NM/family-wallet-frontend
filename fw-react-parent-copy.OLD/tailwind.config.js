/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Base colors
        'bg-primary': '#0a0a0f',
        'bg-card': '#1a1a2e',
        'bg-elevated': '#16213e',
        
        // Neon accents
        'neon-cyan': '#00f5ff',
        'neon-pink': '#ff006e',
        'neon-purple': '#8338ec',
        'neon-green': '#06ffa5',
        
        // Semantic
        'success': '#06ffa5',
        'error': '#ff006e',
        'warning': '#ffbe0b',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}