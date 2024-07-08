import { FC } from 'react'
import styles from './style.module.scss'
import { useNavigate } from 'react-router-dom'

interface ToDoProps {}

const Todo: FC<ToDoProps> = () => {
	const navigate = useNavigate()

	return (
		<div onClick={() => navigate('/todoContent')} className={styles.toDoCard}>
			<h1>TODO SERVICE</h1>
		</div>
	)
}

export default Todo
