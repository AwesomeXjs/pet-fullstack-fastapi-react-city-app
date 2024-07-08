import axios from 'axios'
import { toast } from 'react-hot-toast'
import { Dispatch, SetStateAction } from 'react'

export const universalUrlRegisterAndLogin = (
	url: string,
	username: string | boolean,
	password: string | boolean,
	setOpen: Dispatch<SetStateAction<boolean>>,
	setAuth: Dispatch<SetStateAction<boolean>>,
	setUser: Dispatch<SetStateAction<string | boolean>>,
	goToAuthPage: () => void
) => {
	if (typeof password == "string") {
		if (password.length < 5 || !username) {
			toast.error('Нужно ввести юзернейм и пароль минимум из 5 символов!')
			return
		}
	}

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
			if (response.status == 202) {
				toast.dismiss()
				toast.error('Пользователь с таким юзернеймом уже зарегестрирован!')
				return
			}
			if (response.status == 201) {
				toast.dismiss()
				toast.success(
					`Вы успешно прошли регистрацию! ${response.data.username}, добро пожаловать!`
				)
				setOpen(false)
				setAuth(true)
				setUser(response.data.username)
				console.log(response.data.username)
				goToAuthPage()
				return
			}
			if (response.status == 200) {
				toast.dismiss()
				toast.success('Вы успешно вошли в систему!', {})
				setOpen(false)
				setAuth(true)
				setUser(response.data.username)
				console.log(response.data.username)
				goToAuthPage()
				return
			}
			toast.dismiss()
			return
		})
		.catch(function (error) {
			if (error.response) {
				toast.dismiss()
				toast.error(`${error.response.data.detail}`)
				return
			}
			toast.dismiss()
			toast.error('Что то пошло не так попробуйте позже!')
			setOpen(false)
			return
		})
	toast.loading('Ожидание...')
	return
}

export const logoutUs = (
	url: string,
	setAuth: Dispatch<SetStateAction<boolean>>
) => {
	axios
		.post(url, { withCredentials: true })
		.then(function () {
			toast.dismiss()
			toast.success('Досвидания!')
			setAuth(false)
			return
			
		})
		.catch(function () {
			setAuth(false)
			toast.dismiss()
			toast.success('Досвидания!')
			return
			
		})
	toast.loading('Ожидание...',)
	toast.dismiss()
	return
}
