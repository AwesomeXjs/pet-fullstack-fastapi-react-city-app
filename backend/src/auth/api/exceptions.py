from fastapi import HTTPException, status


def not_accept_406_exc(detail: str):
    not_accept = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )
    return not_accept


def unauth_401_exc(detail: str):
    unregistered_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )
    return unregistered_exc
