/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      width: {
        '3.5/12': '29.16%',
        '1.5/12': '12.5%',
      },
    },
  },
  plugins: [],
}

