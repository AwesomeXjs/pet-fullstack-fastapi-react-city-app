import styles from './styles.module.scss'

import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import { FC, useState } from 'react'
import Button from '@mui/material/Button'
import axios from 'axios'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

interface CreateToDoProps {
	user: string | boolean
}

const CreateToDo: FC<CreateToDoProps> = ({ user }) => {
	const [todoTitle, setTodoTitle] = useState('')
	const [todoDescr, setTodoDescr] = useState('')

	const navigate = useNavigate()

	const createTodoHandler = (_event: React.ChangeEvent<object>) => {
		_event.preventDefault()
		const data_json = JSON.stringify({
			user_username: user,
			title: todoTitle,
			description: todoDescr,
		})
		if (!todoTitle || !todoDescr) {
			toast.error('Нужно ввести название и описание туду!')
			return
		}

		axios({
			method: 'POST',
			url: 'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/v1/todo/create',
			data: data_json,
			headers: {
				'Content-Type': 'application/json',
			},
		})
			.then(function (response) {
				toast.dismiss()
				toast.success(`Туду с названием ${response.data.title} создана!`)
				return
			})
			.catch(function () {
				toast.dismiss()
				toast.error('Что то пошло не так! Попробуйте позже!')
				return
			})

		toast.loading('Ожидание...')
	}

	return (
		<div className={styles.todoContentWrapper}>
			<div className={styles.toDoCard}>
				<Box
					component='form'
					sx={{
						'& .MuiTextField-root': { m: 1, width: '25ch' },
					}}
					noValidate
					autoComplete='off'
				>
					
						<form className={styles.inputWrapper} action=''>
							<TextField
								id='outlined-basic'
								label='Title'
								variant='outlined'
								value={todoTitle}
								onChange={e => setTodoTitle(e.target.value)}
							/>
							<TextField
								id='outlined-multiline-flexible'
								label='Description'
								multiline
								maxRows={6}
								value={todoDescr}
								onChange={e => setTodoDescr(e.target.value)}
							/>
							<div className={styles.btn}>
								<Button type='submit' onClick={createTodoHandler} variant='outlined'>
									Create todo!
								</Button>
							</div>
							<div className={styles.btn}>
								<Button
									onClick={() => navigate('/todoList')}
									variant='outlined'
								>
									Check my todos!
								</Button>
							</div>
						</form>
					
				</Box>
			</div>
		</div>
	)
}

export default CreateToDo
