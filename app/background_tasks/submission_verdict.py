import asyncio

from app.db.enums import MessageTypeEnum
from app.services import ContestApiManager, ProblemStateManager, training_manager
from app.utils import WebSocketMessage


async def get_submission_verdict(
    problem_state_manager: ProblemStateManager,
    oauth_token: str,
    contest_id: str,
    submission_id: str,
    training_session_id: str,
) -> None:
    api_manager = ContestApiManager(authorization=oauth_token)

    while True:
        data, status_code = await api_manager.get_submission_short(
            int(contest_id), int(submission_id)
        )
        if status_code == 200:
            verdict = data.get("verdict")

            await problem_state_manager.adjust_problem_state(
                training_session_id=training_session_id,
                response_content=data,
            )

            if verdict != "No report":
                data["id"] = submission_id
                message = WebSocketMessage(
                    type=MessageTypeEnum.SUBMISSION_VERDICT_RETRIEVED, payload=data
                )
                await training_manager.broadcast(training_session_id, message.json())
                return
        await asyncio.sleep(3)
