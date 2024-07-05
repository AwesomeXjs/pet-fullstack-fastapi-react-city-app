import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		port: 8080,
		proxy: {
			'/auth': {
				target: 'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/',
				changeOrigin: true,
				rewrite: path => path.replace(/^\/api/, '/api'),
			},
		},
	},
})
