from fastapi import APIRouter, Depends
from datetime import datetime
from schemas import BotResponse, RequestSchema
from services.bot_service import BotService
import utils.urls as url
from auth.request_authencator import authencate_request
import json

router = APIRouter()


@router.post(url.TOOL_CALL, response_model=BotResponse)
async def ask_about_product_bot(
    resquest_data: RequestSchema, auth=Depends(authencate_request)
):
    query = resquest_data.user_query
    return await BotService.async_get_bot_response(query)


@router.post(url.RIDDLE, response_model=BotResponse)
async def ask_about_product_bot(
    resquest_data: RequestSchema, auth=Depends(authencate_request)
):
    query = resquest_data.user_query
    return await BotService.async_get_bot_response(query, use_tool=False)


# In-memory session store (use Redis in prod)
# session_store = {}
# @router.post(url.INSTA)  # ,response_model=InstaResponse)
# def ask_question(req: InstaRequest):
#     if req.thread_id and req.thread_id in session_store:
#         crag_instance = session_store[req.thread_id]
#     else:
#         # crag_instance = CRAG()
#         thread_id = f"GB-CRAG:{datetime.now().isoformat()}"
#         crag_instance.thread_id = thread_id
#         session_store[thread_id] = crag_instance

#     out = crag_instance.invoke_crag(req.question)
#     out["thread_id"] = crag_instance.thread_id
#     return out
