import { useState } from 'react'

import Header from './header/header'
import TransitionsModal from './modal/Modal'
import MainPage from './main_page/MainPage'
import AuthPage from './auth_pages/AuthPage'

const App = () => {
	const [open, setOpen] = useState<boolean>(false)
	const [auth, setAuth] = useState<boolean>(false)

	const handleOpen = () => {
		setOpen(true)
	}

	const handleClose = () => {
		setOpen(false)
	}
	return (
		<>
			<div>
				<Header setAuth={setAuth} auth={auth} handleOpen={handleOpen} />
				{!auth ? <MainPage /> : <AuthPage />}
				<TransitionsModal
					setAuth={setAuth}
					setOpen={setOpen}
					open={open}
					handleOpen={handleOpen}
					handleClose={handleClose}
				/>
			</div>
		</>
	)
}

export default App
