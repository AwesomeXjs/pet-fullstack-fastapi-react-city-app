import ReactDOM from 'react-dom/client'
import './scss/_style.scss'
import App from './components/App'
import { Toaster } from 'react-hot-toast'
import {  HashRouter } from 'react-router-dom'




const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
	<>
		<HashRouter>
			<App />
			<Toaster position='bottom-center' reverseOrder={false} />
		</HashRouter>
	</>
)
