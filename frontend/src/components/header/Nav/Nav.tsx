import React, { Dispatch, FC, SetStateAction, useState } from 'react'
import BottomNavigation from '@material-ui/core/BottomNavigation'
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction'
import ExitToAppIcon from '@material-ui/icons/ExitToApp'
import RestoreIcon from '@material-ui/icons/Restore'
import FavoriteIcon from '@material-ui/icons/Favorite'
import LocationOnIcon from '@material-ui/icons/LocationOn'

import styles from './styles.module.scss'
import axios from 'axios'

interface NavProps {
	handleOpen: () => void
	auth: boolean
	setAuth: Dispatch<SetStateAction<boolean>>
}

const LabelBottomNavigation: FC<NavProps> = ({ handleOpen, auth, setAuth }) => {
	const [payload, setPayload] = useState()

	const getPayload = () => {
		axios
			.get('http://localhost:8000/auth/payload')
			.then(function (response) {
				console.log(response.data)
			})
			.catch(function (error) {
				console.log(error)
				setAuth(false)
			})
	}

	const logoutUs = () => {
		axios
			.post('http://localhost:8000/auth/logout', { withCredentials: true })
			.then(function (response) {
				console.log(response)
				setAuth(false)
			})
			.catch(function (error) {
				console.log(error)
			})
	}
	const [value, setValue] = React.useState('')

	const handleChange = (
		_event: React.ChangeEvent<object>,
		newValue: string
	) => {
		setValue(newValue)
	}

	return (
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
				onClick={getPayload}
				label='Nearby'
				value='nearby'
				icon={<LocationOnIcon />}
			/>
			{!auth ? (
				<BottomNavigationAction
					onClick={handleOpen}
					label='Registration'
					value='Registration'
					icon={<ExitToAppIcon />}
				/>
			) : (
				<BottomNavigationAction
					onClick={logoutUs}
					label='Logout'
					value='Logout'
					icon={<ExitToAppIcon />}
				/>
			)}
		</BottomNavigation>
	)
}

export default LabelBottomNavigation
