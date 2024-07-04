import { Dispatch, FC, SetStateAction } from 'react'
import { createStyles, Theme, makeStyles } from '@material-ui/core/styles'
import TextField from '@material-ui/core/TextField'
import Grid from '@material-ui/core/Grid'
import AccountCircle from '@material-ui/icons/AccountCircle'

const useStyles = makeStyles((theme: Theme) =>
	createStyles({
		margin: {
			margin: theme.spacing(1),
		},
	})
)

interface InputFormProps {
	username: string
	setUsername: Dispatch<SetStateAction<string>>
	label: string
}

const InputForm: FC<InputFormProps> = ({ username, setUsername, label }) => {
	const classes = useStyles()

	return (
		<div>
			<div className={classes.margin}>
				<Grid container spacing={1} alignItems='flex-end'>
					<Grid item>
						<AccountCircle />
					</Grid>
					<Grid item>
						<TextField
							value={username}
							onChange={e => setUsername(e.target.value)}
							id='input-with-icon-grid'
							label={label}
						/>
					</Grid>
				</Grid>
			</div>
		</div>
	)
}

export default InputForm
