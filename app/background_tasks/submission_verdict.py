import json
import asyncio

from app.services import ContestApiManager, training_manager
from app.db.enums import MessageTypeEnum



async def get_submission_verdict(oauth_token, contest_id, submission_id, team_id):
    api_manager = ContestApiManager(authorization=oauth_token)

    while True:
        data, status_code = await api_manager.get_submission_short(contest_id, submission_id)
        if status_code == 200:
            verdict = data.get("verdict")
            if verdict != "No report":
                store_key = f"{team_id}_{contest_id}"

                message = {
                    "type": MessageTypeEnum.SUBMISSION_VERDICT_RETRIEVED,
                    "data": data
                }
                await training_manager.broadcast(json.dumps(message), store_key)
                return
        await asyncio.sleep(3)


