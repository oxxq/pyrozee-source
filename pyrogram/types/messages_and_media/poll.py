from datetime import datetime
from typing import List, Union, Optional

import pyrogram
from pyrogram import raw, enums, utils
from pyrogram import types
from ..object import Object
from ..update import Update


class Poll(Object, Update):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        question: str,
        options: List["types.PollOption"],
        question_entities: List["types.MessageEntity"] = None,
        total_voter_count: int,
        is_closed: bool,
        is_anonymous: bool = None,
        type: "enums.PollType" = None,
        allows_multiple_answers: bool = None,
        chosen_option_id: Optional[int] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_entities: Optional[List["types.MessageEntity"]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
    ):
        super().__init__(client)

        self.id = id
        self.question = question
        self.options = options
        self.question_entities = question_entities
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        self.chosen_option_id = chosen_option_id
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.explanation_entities = explanation_entities
        self.open_period = open_period
        self.close_date = close_date

    @staticmethod
    def _parse(
        client,
        media_poll: Union["raw.types.MessageMediaPoll", "raw.types.UpdateMessagePoll"],
    ) -> "Poll":
        poll: raw.types.Poll = media_poll.poll
        poll_results: raw.types.PollResults = media_poll.results
        results: List[raw.types.PollAnswerVoters] = poll_results.results

        chosen_option_id = None
        correct_option_id = None
        options = []

        for i, answer in enumerate(poll.answers):
            voter_count = 0

            if results:
                result = results[i]
                voter_count = result.voters

                if result.chosen:
                    chosen_option_id = i

                if result.correct:
                    correct_option_id = i

            o_entities = (
                [
                    types.MessageEntity._parse(client, entity, {})
                    for entity in answer.text.entities
                ]
                if answer.text.entities
                else []
            )
            option_entities = types.List(filter(lambda x: x is not None, o_entities))

            options.append(
                types.PollOption(
                    text=answer.text.text,
                    voter_count=voter_count,
                    data=answer.option,
                    entities=option_entities,
                    client=client,
                )
            )

        q_entities = (
            [
                types.MessageEntity._parse(client, entity, {})
                for entity in poll.question.entities
            ]
            if poll.question.entities
            else []
        )
        question_entities = types.List(filter(lambda x: x is not None, q_entities))

        return Poll(
            id=str(poll.id),
            question=poll.question.text,
            options=options,
            question_entities=question_entities,
            total_voter_count=media_poll.results.total_voters,
            is_closed=poll.closed,
            is_anonymous=not poll.public_voters,
            type=enums.PollType.QUIZ if poll.quiz else enums.PollType.REGULAR,
            allows_multiple_answers=poll.multiple_choice,
            chosen_option_id=chosen_option_id,
            correct_option_id=correct_option_id,
            explanation=poll_results.solution,
            explanation_entities=(
                [
                    types.MessageEntity._parse(client, i, {})
                    for i in poll_results.solution_entities
                ]
                if poll_results.solution_entities
                else None
            ),
            open_period=poll.close_period,
            close_date=utils.timestamp_to_datetime(poll.close_date),
            client=client,
        )

    @staticmethod
    def _parse_update(client, update: "raw.types.UpdateMessagePoll"):
        if update.poll is not None:
            return Poll._parse(client, update)

        results = update.results.results
        chosen_option_id = None
        correct_option_id = None
        options = []

        for i, result in enumerate(results):
            if result.chosen:
                chosen_option_id = i

            if result.correct:
                correct_option_id = i

            options.append(
                types.PollOption(
                    text="",
                    voter_count=result.voters,
                    data=result.option,
                    client=client,
                )
            )

        return Poll(
            id=str(update.poll_id),
            question="",
            options=options,
            total_voter_count=update.results.total_voters,
            is_closed=False,
            chosen_option_id=chosen_option_id,
            correct_option_id=correct_option_id,
            client=client,
        )

    async def stop(
        self,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None,
    ) -> "types.Poll":
        """Bound method *stop* of :obj:`~pyrogram.types.Poll`.

        Use as a shortcut for:

        .. code-block:: python

            client.stop_poll(
                chat_id=message.chat.id,
                message_id=message.id,
            )

        Parameters:
            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.

        Example:
            .. code-block:: python

                message.poll.stop()

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the stopped poll with the final results is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.stop_poll(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup,
            business_connection_id=(
                self.business_connection_id
                if business_connection_id is None
                else business_connection_id
            ),
        )
