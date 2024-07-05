import ReactDOM from 'react-dom/client'
import './scss/_style.scss'
import App from './components/App'
import { Toaster } from 'react-hot-toast'
import React from 'react'
import { BrowserRouter } from 'react-router-dom'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
	<>
		<React.StrictMode>
			<BrowserRouter basename='/'>
				<App />
				<Toaster position='bottom-center' reverseOrder={false} />
			</BrowserRouter>
		</React.StrictMode>
	</>
)
