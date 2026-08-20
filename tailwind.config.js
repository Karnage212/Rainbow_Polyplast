/** @type {import('tailwindcss').Config} */
export default {
      content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
      theme: {
        extend: {
          colors: {
            brand: {
              purple: '#49326B',
              green: '#039544',
              yellow: '#FEF111',
              red: '#E5332E',
              black: '#0B0B0C',
              white: '#FFFFFF'
            }
          },
          fontFamily: {
            sans: ['DM Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          blur: {
            'xs': '2px',
          }
        }
      }
    };
