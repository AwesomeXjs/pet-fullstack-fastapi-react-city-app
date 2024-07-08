import { useState, useEffect } from 'react'

import Header from './header/header'
import TransitionsModal from './modal/Modal'
import MainPage from './main_page/MainPage'
import styles from './app.module.scss'

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import video from '../assets/NatureBack.mp4'
import { Route, Routes } from 'react-router-dom'
import NotFoundPage from './NotFoundPage/NotFoundPage'
import PrivateRouter from './router/privateRouter'
import AuthPage from './auth_pages/AuthPage'
import ToDoContent from './auth_pages/services/todo/ToDoContent/ToDoContent'
import MyToDoList from './auth_pages/services/todo/ToDoContent/MyToDoList/MyToDoList'
import CreateToDo from './auth_pages/services/todo/ToDoContent/CreateTodo/CreateToDo'

const App = () => {
	const [open, setOpen] = useState<boolean>(false)
	const [auth, setAuth] = useState<boolean>(true)
	const [user, setUser] = useState<string | boolean>(false)

	useEffect(() => {
		if (!user) {
			setAuth(false)
		}
	}, [user])

	// eslint-disable-next-line @typescript-eslint/ban-ts-comment
	// @ts-expect-error
	const [todos, setTodos] = useState<[ToDo]>([])

	const handleOpen = () => {
		setOpen(true)
	}

	const handleClose = () => {
		setOpen(false)
	}
	return (
		<>
			<video autoPlay muted loop className={styles.WelcomeVideo}>
				<source src={video} type='video/mp4' />
			</video>
			<Header handleOpen={handleOpen} auth={auth} setAuth={setAuth} />
			<Routes>
				<Route path='*' element={<NotFoundPage />} />
				<Route path='/' element={<MainPage setOpen={setOpen} />} index />
				<Route element={<PrivateRouter auth={auth} />}>
					<Route path='userPage' element={<AuthPage />}></Route>
					<Route path='todoContent' element={<ToDoContent />} />
					<Route
						path='todoList'
						element={
							<MyToDoList user={user} setTodos={setTodos} todos={todos} />
						}
					/>
					<Route path='createTodo' element={<CreateToDo user={user} />} />
				</Route>
			</Routes>
			<TransitionsModal
				setUser={setUser}
				setAuth={setAuth}
				setOpen={setOpen}
				open={open}
				handleOpen={handleOpen}
				handleClose={handleClose}
			/>
		</>
	)
}

export default App
