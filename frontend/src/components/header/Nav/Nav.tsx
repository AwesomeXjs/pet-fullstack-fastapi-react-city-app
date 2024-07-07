import React, { Dispatch, FC, SetStateAction } from 'react'
import BottomNavigation from '@material-ui/core/BottomNavigation'
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction'
import RestoreIcon from '@material-ui/icons/Restore'
import FavoriteIcon from '@material-ui/icons/Favorite'
import LocationOnIcon from '@material-ui/icons/LocationOn'
import LoginIcon from '@mui/icons-material/Login'
import LogoutIcon from '@mui/icons-material/Logout'
import 'react-toastify/dist/ReactToastify.css'

import styles from './styles.module.scss'
import { logoutUs } from '../../../api_service/api_service'

interface NavProps {
	handleOpen: () => void
	auth: boolean
	setAuth: Dispatch<SetStateAction<boolean>>
}

const LabelBottomNavigation: FC<NavProps> = ({ handleOpen, auth, setAuth }) => {
	const logoutFx = () => {
		logoutUs('/auth/logout', setAuth)
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
					label='Recents'
					value='recents'
					icon={<RestoreIcon />}
				/>
				<BottomNavigationAction
					label='Favorites'
					value='favorites'
					icon={<FavoriteIcon />}
				/>
				<BottomNavigationAction
					label='Nearby'
					value='nearby'
					icon={<LocationOnIcon />}
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
