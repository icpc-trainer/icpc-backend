from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.connection import get_session
from app.db.models import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_comment(
        self,
        user_id: UUID,
        training_session_id: UUID,
        problem_alias: str,
        content: str,
    ) -> Comment:
        comment = Comment(
            user_id=user_id,
            problem_alias=problem_alias,
            training_session_id=training_session_id,
            content=content,
        )
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_comments(
        self,
        training_session_id: UUID,
        problem_alias: str,
    ) -> List[Comment]:
        query = select(Comment).filter_by(
            training_session_id=training_session_id,
            problem_alias=problem_alias,
        )
        return (await self.session.scalars(query)).all()

