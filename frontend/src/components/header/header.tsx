import { Dispatch, FC, SetStateAction } from 'react'

import LabelBottomNavigation from './Nav/Nav'
import styles from './header.module.scss'

interface HeaderProps {
	handleOpen: () => void
	auth: boolean
	setAuth: Dispatch<SetStateAction<boolean>>
}

const Header: FC<HeaderProps> = ({ handleOpen, auth, setAuth }) => {
	return (
		<div className={styles.headerMain}>
			<LabelBottomNavigation
				setAuth={setAuth}
				auth={auth}
				handleOpen={handleOpen}
			/>
		</div>
	)
}

export default Header
