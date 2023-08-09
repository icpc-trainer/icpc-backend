import json
import asyncio

from app.services import ContestApiManager, training_manager
from app.db.enums import MessageTypeEnum
from app.utils import WebSocketMessage



async def get_submission_verdict(oauth_token, contest_id, submission_id, training_session_id):
    api_manager = ContestApiManager(authorization=oauth_token)

    while True:
        data, status_code = await api_manager.get_submission_short(contest_id, submission_id)
        if status_code == 200:
            verdict = data.get("verdict")
            if verdict != "No report":
                data["id"] = submission_id
                message = WebSocketMessage(
                    type=MessageTypeEnum.SUBMISSION_VERDICT_RETRIEVED,
                    payload=data
                )
                await training_manager.broadcast(training_session_id, message.json())
                return
        await asyncio.sleep(3)


