import { FC } from 'react'
import { Navigate, Outlet } from 'react-router-dom'

interface privateProps {
	auth: boolean
}

const PrivateRouter: FC<privateProps> = ({ auth }) => {
	return auth ? <Outlet /> : <Navigate to='/' />
}

export default PrivateRouter
