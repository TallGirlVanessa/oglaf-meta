/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./oglaf/templates/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}
