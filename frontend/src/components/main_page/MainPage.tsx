import { Dispatch, FC, SetStateAction, useEffect, useState } from 'react'
import styles from './styles.module.scss'
import Button from '@mui/material/Button'

interface MainPageProps {
	setOpen: Dispatch<SetStateAction<boolean>>
}


const MainPage: FC<MainPageProps> = ({ setOpen }) => {
	const time = new Date()
	const [clock, setClock] = useState(time)
	const tick = () => {
		setClock(new Date())
	}
	const thisTimer = () => {
		setInterval(() => {
			tick()
		}, 40000)
	}
	useEffect(() => {
		thisTimer()
		return () => {
			// eslint-disable-next-line @typescript-eslint/ban-ts-comment
			// @ts-expect-error
			clearInterval(thisTimer)
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])
	return (
		<>
			<div className={`${styles.mainPageText} container`}>
				<div className={styles.clockWrapper}>
					<span>
						{clock.getHours() >= 10 ? clock.getHours() : `0${clock.getHours()}`}
						:
					</span>
					<span>
						{clock.getMinutes() >= 10
							? clock.getMinutes()
							: `0${clock.getMinutes()}`}
					</span>
				</div>
				<div>
					<Button onClick={() => setOpen(true)} variant='contained'>Войти в аккаунт</Button>
				</div>
			</div>
		</>
	)
}

export default MainPage
