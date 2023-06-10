import typing

import anyio

from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import ContentStream, Response, StreamingResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi import Request

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]
DispatchFunction = typing.Callable[
    [Request, RequestResponseEndpoint], typing.Awaitable[Response]
]
T = typing.TypeVar("T")


class SixBaseHTTPMiddleware:
    def __init__(
        self, app: ASGIApp, dispatch: typing.Optional[DispatchFunction] = None
    ) -> None:
        self.app = app
        self.dispatch_func = self.dispatch if dispatch is None else dispatch

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        response_sent = anyio.Event()

        async def call_next(status_code, content, raw_headers, info) -> Response:
            response = Response(
                status_code=status_code, content=content, headers=raw_headers
            )
            return response

        async with anyio.create_task_group() as task_group:
            request = Request(scope, receive=receive)
            response = await self.dispatch_func(request, call_next)
            await response(scope, receive, send)
            response_sent.set()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        raise NotImplementedError()  # pragma: no cover


class _StreamingResponse(StreamingResponse):
    def __init__(
        self,
        content: ContentStream,
        status_code: int = 200,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
        info: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None:
        self._info = info
        super().__init__(content, status_code, headers, media_type, background)

    async def stream_response(self, send: Send) -> None:
        if self._info:
            await send({"type": "http.response.debug", "info": self._info})
        return await super().stream_response(send)
