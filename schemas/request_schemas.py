from pydantic import BaseModel


class RequestSchema(BaseModel):
    user_query: str
