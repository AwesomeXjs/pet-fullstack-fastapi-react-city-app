import axios from 'axios'
import { toast } from 'react-hot-toast'
import { Dispatch, SetStateAction } from 'react'

export const universalUrlRegisterAndLogin = (
	url: string,
	username: string | boolean,
	password: string | boolean,
	setOpen: Dispatch<SetStateAction<boolean>>,
	setAuth: Dispatch<SetStateAction<boolean>>
) => {
	const data_json = JSON.stringify({ username: username, password: password })
	if (!password || !username) {
		toast.error('Нужно ввести юзернейм и пароль!')
		return
	}
	const my_prom = axios({
		method: 'POST',
		url: url,
		data: data_json,
		headers: {
			'Content-Type': 'application/json',
		},
	})
		.then(function (response) {
			if (response.status == 202) {
				toast.error('Пользователь с таким юзернеймом уже зарегестрирован!')
				return
			}
			if (response.status == 201) {
				toast.success(
					`Вы успешно прошли регистрацию! ${response.data.username}, добро пожаловать!`
				)
				setOpen(false)
				setAuth(true)
				return
			}
			if (response.status == 200) {
				toast.success('Вы успешно вошли в систему!', {})
				setOpen(false)
				setAuth(true)
				return
			}
			console.log(response)
		})
		.catch(function () {
			toast.error('Что то пошло не так попробуйте позже!')
			setOpen(false)
		})

	toast.promise(my_prom, {
		loading: 'Ожидание...',
		success: 'Ответ получен!',
		error: 'Could not save.',
	})
}

export const logoutUs = (
	url: string,
	setAuth: Dispatch<SetStateAction<boolean>>
) => {
	const my_prom = axios
		.post(url, { withCredentials: true })
		.then(function () {
			toast.success('Досвидания!')
			setAuth(false)
		})
		.catch(function () {
			setAuth(false)
			toast.success('Досвидания!')
		})
	toast.promise(my_prom, {
		loading: 'Ожидание...',
		success: 'Ответ получен!',
		error: 'Could not save.',
	})
}
