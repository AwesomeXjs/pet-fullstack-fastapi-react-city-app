import React, { Dispatch, FC, SetStateAction } from 'react'
import { makeStyles, Theme, createStyles } from '@material-ui/core/styles'
import Modal from '@material-ui/core/Modal'
import Backdrop from '@material-ui/core/Backdrop'
import Fade from '@material-ui/core/Fade'
import RegistrtionForm from '../registration_form/RegistrationForm'

const useStyles = makeStyles((theme: Theme) =>
	createStyles({
		modal: {
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
		},
		paper: {
			backgroundColor: theme.palette.background.paper,
			border: '2px solid #000',
			boxShadow: theme.shadows[5],
			padding: theme.spacing(2, 4, 3),
		},
	})
)

export interface ModalProps {
	handleOpen: () => void
	handleClose: () => void
	open: boolean
	setOpen: Dispatch<SetStateAction<boolean>>
	setAuth: Dispatch<SetStateAction<boolean>>
}

const TransitionsModal: FC<ModalProps> = ({
	handleClose,
	open,
	setOpen,
	setAuth,
}) => {
	const classes = useStyles()

	return (
		<div>
			<Modal
				aria-labelledby='transition-modal-title'
				aria-describedby='transition-modal-description'
				className={`${classes.modal}`}
				open={open}
				onClose={handleClose}
				closeAfterTransition
				BackdropComponent={Backdrop}
				BackdropProps={{
					timeout: 500,
				}}
			>
				<Fade in={open}>
					<div className={`${classes.paper}`}>
						{/* Любой компонент для модалки */}
						<RegistrtionForm setOpen={setOpen} setAuth={setAuth} />
					</div>
				</Fade>
			</Modal>
		</div>
	)
}

export default TransitionsModal
