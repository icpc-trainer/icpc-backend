from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> list[Comment]:
        query = select(Comment).filter_by(
            training_session_id=training_session_id,
            problem_alias=problem_alias,
        )
        return list((await self.session.scalars(query)).all())

    async def delete_comment(
        self,
        comment_id: str,
    ) -> None:
        delete_query = delete(Comment).where(Comment.id == comment_id)
        await self.session.execute(delete_query)
        await self.session.commit()
