/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0B1F44',
        navy: '#15336B',
        cyanx: '#16BFE5',
        greenx: '#43E864',
        indigox: '#5866F2',
        paper: '#F6F8FC'
      },
      boxShadow: {
        soft: '0 18px 50px rgba(11,31,68,.10)'
      }
    }
  },
  plugins: []
};
