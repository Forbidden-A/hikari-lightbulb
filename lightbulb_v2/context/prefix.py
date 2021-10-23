# -*- coding: utf-8 -*-
# Copyright © tandemdude 2020-present
#
# This file is part of Lightbulb.
#
# Lightbulb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lightbulb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Lightbulb. If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

__all__ = ["PrefixContext"]

import typing as t

import hikari

from lightbulb_v2.context import base

if t.TYPE_CHECKING:
    from lightbulb_v2 import app as app_
    from lightbulb_v2 import commands


class PrefixContext(base.Context):
    def __init__(
        self,
        app: app_.BotApp,
        event: hikari.MessageCreateEvent,
        command: t.Optional[commands.prefix.PrefixCommand],
        invoked_with: str,
        prefix: str,
    ) -> None:
        super().__init__(app)
        self._event = event
        self._command = command
        self._invoked_with = invoked_with
        self._prefix = prefix
        self._options: t.Dict[str, t.Any] = {}

    @property
    def event(self) -> hikari.MessageCreateEvent:
        return self._event

    @property
    def raw_options(self) -> t.Dict[str, t.Any]:
        return self._options

    @property
    def options(self) -> base.OptionsProxy:
        return base.OptionsProxy(self.raw_options)

    @property
    def channel_id(self) -> hikari.Snowflakeish:
        return self.event.message.channel_id

    @property
    def guild_id(self) -> t.Optional[hikari.Snowflakeish]:
        return self.event.message.guild_id

    @property
    def member(self) -> t.Optional[hikari.Member]:
        return self.event.message.member

    @property
    def author(self) -> hikari.User:
        return self.event.message.author

    @property
    def invoked_with(self) -> str:
        return self._invoked_with

    @property
    def command(self) -> t.Optional[commands.prefix.PrefixCommand]:
        return self._command

    def get_channel(self) -> t.Optional[t.Union[hikari.GuildChannel, hikari.Snowflake]]:
        if self.guild_id is not None:
            return self.app.cache.get_guild_channel(self.channel_id)
        return self.app.cache.get_dm_channel_id(self.author.id)

    async def respond(self, *args: t.Any, **kwargs: t.Any) -> hikari.Message:
        return await self.event.message.respond(*args, **kwargs)