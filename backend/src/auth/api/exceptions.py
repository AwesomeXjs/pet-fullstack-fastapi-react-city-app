from fastapi import HTTPException, status

unique_error = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail=f"Такой логин или емаил уже существует!",
)

something_wrong = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail=f"Что то пошло не так, проверьте подключение к интернету!",
)
