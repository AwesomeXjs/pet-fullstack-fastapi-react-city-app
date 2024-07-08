import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

//https://vitejs.dev/config/
export default defineConfig({
	assetsInclude: ['**/*.mp4'],
	plugins: [react()],
	server: {
		port: 10000,
		proxy: {
			'/auth': {
				target: 'https://pet-fullstack-fastapi-react-city-app-1.onrender.com',
				changeOrigin: true,
				rewrite: path => path.replace(/^\/auth/, '/auth'),
			},
			'/v1': {
				target: 'https://pet-fullstack-fastapi-react-city-app-1.onrender.com',
				changeOrigin: true,
				rewrite: path => path.replace(/^\/v1/, '/v1'),
			},
		},
	},
})
