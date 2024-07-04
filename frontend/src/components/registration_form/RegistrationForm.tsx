import React, {
	ChangeEventHandler,
	FC,
	Dispatch,
	SetStateAction,
	useState,
} from 'react'
import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'
import Button from '@material-ui/core/Button'
import InputForm from './input/InputForm'
import axios from 'axios'

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
}

const RegistrtionForm: FC<RegisterProps> = ({ setOpen, setAuth }) => {
	const [value, setValue] = useState(0)
	const [label, setLabel] = useState('Регистрация')

	const [username, setUsername] = useState('')
	const [password, setPassword] = useState('')

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

	const universalUrlRegisterAndLogin = (url: string) => {
		const data_json = JSON.stringify({ username: username, password: password })
		axios({
			method: 'POST',
			url: url,
			data: data_json,
			headers: {
				'Content-Type': 'application/json',
			},
		})
			.then(function (response) {
				console.log(response)
				setOpen(false)
				setAuth(true)
			})
			.catch(function (error) {
				console.log(error)
			})
	}

	const registerAndLoginHandler = () => {
		if (label == 'Регистрация') {
			universalUrlRegisterAndLogin('http://localhost:8000/auth/register')
			return
		} else {
			universalUrlRegisterAndLogin('http://localhost:8000/auth/login')
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
				<TabPanel value={value} index={0}>
					<InputForm
						label='Введите ваш username'
						username={username}
						setUsername={setUsername}
					/>
					<InputForm
						label='Введите ваш пароль'
						username={password}
						setUsername={setPassword}
					/>
				</TabPanel>
				<TabPanel value={value} index={1}>
					<InputForm
						label='Введите ваш username'
						username={username}
						setUsername={setUsername}
					/>
					<InputForm
						label='Введите ваш пароль'
						username={password}
						setUsername={setPassword}
					/>
				</TabPanel>
			</div>
			<Button
				onClick={registerAndLoginHandler}
				variant='contained'
				color='primary'
			>
				{label}
			</Button>
		</>
	)
}

export default RegistrtionForm
