import React, { Dispatch, FC, SetStateAction } from 'react'
import BottomNavigation from '@material-ui/core/BottomNavigation'
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction'
import LoginIcon from '@mui/icons-material/Login'
import LogoutIcon from '@mui/icons-material/Logout'
import 'react-toastify/dist/ReactToastify.css'
import { useNavigate } from 'react-router-dom'
import ComputerIcon from '@mui/icons-material/Computer'

import styles from './styles.module.scss'
import { logoutUs } from '../../../api_service/api_service'

interface NavProps {
	handleOpen: () => void
	auth: boolean
	setAuth: Dispatch<SetStateAction<boolean>>
}

const LabelBottomNavigation: FC<NavProps> = ({ handleOpen, auth, setAuth }) => {
	const navigate = useNavigate()

	const logoutFx = () => {
		logoutUs(
			'https://pet-fullstack-fastapi-react-city-app-1.onrender.com/auth/logout',
			setAuth
		)
	}

	const [value, setValue] = React.useState('')

	const handleChange = (
		_event: React.ChangeEvent<object>,
		newValue: string
	) => {
		setValue(newValue)
	}

	return (
		<>
			<BottomNavigation
				value={value}
				onChange={handleChange}
				className={`${styles.nav_main_style}`}
			>
				<BottomNavigationAction
					onClick={() => navigate('/userPage')}
					label='Services'
					value='recents'
					icon={<ComputerIcon />}
				/>

				{!auth ? (
					<BottomNavigationAction
						onClick={handleOpen}
						label='Registration'
						value='Registration'
						icon={<LoginIcon />}
					/>
				) : (
					<BottomNavigationAction
						onClick={logoutFx}
						label='Logout'
						value='Logout'
						icon={<LogoutIcon />}
					/>
				)}
			</BottomNavigation>
		</>
	)
}

export { LabelBottomNavigation }
