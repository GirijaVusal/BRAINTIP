from pydantic import BaseModel
from typing import Optional, List, Dict, Union


class BotResponse(BaseModel):
    code: int
    response: Union[str, Dict]
    token_usage: Optional[List[Dict]] = None
    thread_id: Optional[str] = None
