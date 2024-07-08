import React, { FC, Dispatch, SetStateAction, useState } from 'react'
import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'
import Button from '@material-ui/core/Button'
import InputForm from './input/InputForm'
import { universalUrlRegisterAndLogin } from '../../api_service/api_service'
import { useNavigate } from 'react-router-dom'
import styles from './styles.module.scss'


interface TabPanelProps {
	children?: React.ReactNode
	index: unknown
	value: unknown
}

function TabPanel(props: TabPanelProps) {
	const { children, value, index, ...other } = props

	return (
		<div
			role='tabpanel'
			hidden={value !== index}
			id={`simple-tabpanel-${index}`}
			aria-labelledby={`simple-tab-${index}`}
			{...other}
		>
			{value === index && (
				<Box p={3}>
					<Typography>{children}</Typography>
				</Box>
			)}
		</div>
	)
}

function a11yProps(index: unknown) {
	return {
		id: `simple-tab-${index}`,
		'aria-controls': `simple-tabpanel-${index}`,
	}
}

interface RegisterProps {
	setOpen: Dispatch<SetStateAction<boolean>>
	setAuth: Dispatch<SetStateAction<boolean>>
	setUser: Dispatch<SetStateAction<string | boolean>>
}

const RegistrtionForm: FC<RegisterProps> = ({ setOpen, setAuth, setUser }) => {
	const [value, setValue] = useState(0)
	const [label, setLabel] = useState('Регистрация')

	const [username, setUsername] = useState<string | boolean>('')
	const [password, setPassword] = useState<string | boolean>('')

	const navigate = useNavigate()

	const goToAuth = () => navigate('/userPage')

	const setLabelLogin = () => {
		setLabel('Войти')
	}
	const setLabelReg = () => {
		setLabel('Регистрация')
	}

	const handleChange = (
		_event: React.ChangeEvent<object>,
		newValue: number
	) => {
		setValue(newValue)
	}

	const registerAndLoginHandler = (_event: React.ChangeEvent<object>) => {
		_event.preventDefault()
		if (label == 'Регистрация') {
			universalUrlRegisterAndLogin(
				'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/auth/register',
				username,
				password,
				setOpen,
				setAuth,
				setUser,
				goToAuth
			)
			return
		} else {
			universalUrlRegisterAndLogin(
				'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/auth/login',
				username,
				password,
				setOpen,
				setAuth,
				setUser,
				goToAuth
			)
		}
	}

	return (
		<>
			<div>
				<AppBar position='static'>
					<Tabs
						value={value}
						onChange={handleChange}
						aria-label='simple tabs example'
					>
						<Tab onClick={setLabelReg} label='Регистрация' {...a11yProps(0)} />
						<Tab onClick={setLabelLogin} label='Вход' {...a11yProps(1)} />
					</Tabs>
				</AppBar>
				<form onSubmit={registerAndLoginHandler} action=''>
					<TabPanel value={value} index={0}>
						<InputForm
							type='text'
							label='Введите ваш username'
							username={username}
							setUsername={setUsername}
						/>
						<InputForm
						type='password'
							label='Введите ваш пароль'
							username={password}
							setUsername={setPassword}
						/>
					</TabPanel>
					<TabPanel value={value} index={1}>
						<div>
							<InputForm
								type='text'
								label='Введите ваш username'
								username={username}
								setUsername={setUsername}
							/>

							<InputForm
								type='password'
								label='Введите ваш пароль'
								username={password}
								setUsername={setPassword}
							/>
						</div>
					</TabPanel>
					<div className={styles.btn}>
						<Button
							type='submit'
							onClick={registerAndLoginHandler}
							variant='contained'
							color='primary'
						>
							{label}
						</Button>
					</div>
				</form>
			</div>
		</>
	)
}

export default RegistrtionForm
