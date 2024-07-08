import { Dispatch, FC, SetStateAction, useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardActions from '@mui/material/CardActions'
import CardContent from '@mui/material/CardContent'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import styles from './styles.module.scss'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import toast from 'react-hot-toast'
import { createStyles, makeStyles, TextField, Theme } from '@material-ui/core'
import Modal from '@material-ui/core/Modal'
import Backdrop from '@material-ui/core/Backdrop'
import Fade from '@material-ui/core/Fade'


const useStyles = makeStyles((theme: Theme) =>
	createStyles({
		modal: {
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			borderRadius: '20px',
		},
		paper: {
			backgroundColor: theme.palette.background.paper,
			border: '2px solid #000',
			boxShadow: theme.shadows[5],
			
			borderRadius: '20px',
		},
	})
)

interface Todo {
	id: string
	title: string
	description: string
}

interface MyToDoListProps {
	todos: [Todo]
	user: string | boolean
	setTodos: Dispatch<SetStateAction<[Todo]>>
}

const MyToDoList: FC<MyToDoListProps> = ({ todos, setTodos, user }) => {
	const classes = useStyles()

	const [modalOpen, setModalOpen] = useState<boolean>(false)
	const [updateTodo, setUpdateToDo] = useState<number>(0)

	const [currentTodoID, setCurrentTodoID] = useState<string>('')

	const modalCloseHandler = () => {
		setModalOpen(false)
	}
	const modalUpdateOpen = (currentTodoID: string, title:string, descr: string) => {
		setModalOpen(true)
		setCurrentTodoID(currentTodoID)
		setCurrentTitle(title)
		setCurrentDesc(descr)
	}

	useEffect(() => {
		axios
			.get(
				`https://pet-fullstack-fastapi-react-city-app-1.onrender.com/v1/todo/all_of_user?username=${user}`
			)
			.then(response => {
				setTodos(response.data)
			})
			.catch(() => {
				toast.error('Что то пошло не так, попробуйте позже!')
			})
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [updateTodo])

	const deleteTodoHandler = (id: string) => {
		axios
			.delete(
				'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/v1/todo/del',
				{ params: { id: id } }
			)
			.then(response => {
				if (response.data == null) {
					toast.success(`Такой тудушки нет!`)
					setUpdateToDo(updateTodo + 1)
					return
				}
				toast.success(`Туду ${response.data} удалена`)
				setUpdateToDo(updateTodo + 1)
			})
			.catch(() => {
				toast.error('Что то пошло не так, попробуйте позже!')
			})
	}

	const [currentTitle, setCurrentTitle] = useState('')
	const [currentDesc, setCurrentDesc] = useState('')

	const updateToDoHandler = (id: string) => {
		if (!currentTitle || !currentDesc) {
			toast.error(`Нужно ввести название и описание!`)
			return
		}
		
		axios
			.patch(
				`https://pet-fullstack-fastapi-react-city-app-1.onrender.com/v1/todo/patch?id=${id}`,
				{
					title: currentTitle,
					description: currentDesc,
				},
				{
					headers: {
						'Content-Type': 'application/json',
					},
				}
			)
			.then(response => {
				if (response.data == null) {
					toast.success(`Такой тудушки нет!`)
					setUpdateToDo(updateTodo + 1)
					return
				}
				toast.success(
					`Туду с названием ${response.data.old_data.title} и описанием ${response.data.old_data.description} обновлена на новую с названием ${response.data.new_data.title} и описанием ${response.data.new_data.description}`
				)
				setUpdateToDo(updateTodo + 1)
			})
			.catch(() => {
				toast.error('Что то пошло не так, попробуйте позже!')
			})
	}

	const navigate = useNavigate()
	return (
		<>
			<div className={styles.toDoLostWrapper}>
				{todos.length ? (
					todos.map(el => {
						return (
							<div className={styles.toDoCard}>
								<Box sx={{ minWidth: 275 }}>
									<Card variant='outlined'>
										<CardContent>
											<Typography
												sx={{ fontSize: 14 }}
												color='text.secondary'
												gutterBottom
											>
												{el.title}
											</Typography>
											<Typography variant='body2'>{el.description}</Typography>
										</CardContent>
										<CardActions>
											<Button
												onClick={() => deleteTodoHandler(el.id)}
												size='small'
											>
												Удалить
											</Button>
											<Button
												onClick={() =>
													modalUpdateOpen(el.id, el.title, el.description)
												}
												size='small'
											>
												Обновить
											</Button>
										</CardActions>
									</Card>
								</Box>
							</div>
						)
					})
				) : (
					<div
						onClick={() => navigate('/createTodo')}
						className={styles.toDoNotFound}
					>
						У вас еще нет тудушек!
					</div>
				)}
				<Modal
					aria-labelledby='transition-modal-title'
					aria-describedby='transition-modal-description'
					className={`${classes.modal} ${styles.modal}`}
					open={modalOpen}
					onClose={modalCloseHandler}
					closeAfterTransition
					BackdropComponent={Backdrop}
					BackdropProps={{
						timeout: 500,
					}}
				>
					<Fade in={modalOpen}>
						<div className={`${classes.paper}`}>
							{/* Любой компонент для модалки */}
							<div className={styles.toDoCard}>
								<Box
									component='form'
									sx={{
										'& .MuiTextField-root': { m: 1, width: '25ch' },
									}}
									noValidate
									autoComplete='off'
								>
									<form
										onSubmit={(e) => {
											e.preventDefault()
											updateToDoHandler(currentTodoID)
										} }
										className={styles.inputWrapper}
										action=''
									>
										<TextField
											id='outlined-basic'
											label='Title'
											variant='outlined'
											value={currentTitle}
											onChange={e => setCurrentTitle(e.target.value)}
										/>
										<TextField
											id='outlined-multiline-flexible'
											label='Description'
											multiline
											maxRows={6}
											value={currentDesc}
											onChange={e => setCurrentDesc(e.target.value)}
										/>
										<div className={styles.btn}>
											<Button
												type='submit'
												onClick={(e) => {
													e.preventDefault()
													updateToDoHandler(currentTodoID)}}
												variant='outlined'
											>
												Update todo!
											</Button>
										</div>
										<div className={styles.btn}>
											<Button
												onClick={() => setModalOpen(false)}
												variant='outlined'
											>
												Check my todos!
											</Button>
										</div>
									</form>
								</Box>
							</div>
						</div>
					</Fade>
				</Modal>
			</div>
			<div className={styles.buttonWrapper}>
				<Button onClick={() => navigate('/createTodo')} variant='contained'>
					Create new todos!
				</Button>
			</div>
		</>
	)
}

export default MyToDoList
