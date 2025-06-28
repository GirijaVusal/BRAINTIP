from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from auth.token_generator import generate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authencate_request(token: str = Depends(oauth2_scheme)):
    if token != generate_token():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
