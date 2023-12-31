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
            # отправка информации о вердикте
            verdict = data.get("verdict")
            data["id"] = submission_id
            message = WebSocketMessage(
                type=MessageTypeEnum.SUBMISSION_VERDICT_RETRIEVED, payload=data
            )
            await training_manager.broadcast(training_session_id, message.json())

            # изменение статуса задачи, когда получаем ее вердикт
            if verdict != "No report":
                await problem_state_manager.adjust_problem_state(
                    training_session_id=training_session_id,
                    response_content=data,
                )
                problem_state = await problem_state_manager.problem_state_repository.get_problem(
                    training_session_id=training_session_id,
                    alias=data.get("problemAlias"),
                )
                db_problem_status = problem_state.status
                message = WebSocketMessage(
                    type=MessageTypeEnum.PROBLEM_STATUS_UPDATED,
                    payload={
                        "status": db_problem_status,
                        "problemAlias": data.get("problemAlias"),
                    }
                )
                await training_manager.broadcast(training_session_id, message.json())

                message = WebSocketMessage(
                    type=MessageTypeEnum.PROBLEM_ATTEMPTS_UPDATED,
                    payload={
                        "attempts": problem_state.attempts,
                        "problemAlias": data.get("problemAlias"),
                    }
                )
                await training_manager.broadcast(training_session_id, message.json())
                return
        await asyncio.sleep(3)
