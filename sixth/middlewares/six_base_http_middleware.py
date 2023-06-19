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

        async def call_next(status_code, content, raw_headers, use_response: bool = True) -> Response:
            if use_response:
                response = Response(
                    status_code=status_code, content=content, headers=raw_headers
                )
                return response
            else:
                return content, raw_headers

        async with anyio.create_task_group() as task_group:
            request = Request(scope, receive=receive)
            response = await self.dispatch_func(request, call_next)
            await response(scope, receive, send)
            response_sent.set()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        raise NotImplementedError()  # pragma: no cover

class SixRateLimitHTTPMiddleware:
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
        send_stream, recv_stream = anyio.create_memory_object_stream()
        app_exc: typing.Optional[Exception] = None
        async def receive_or_disconnect() -> Message:
                if response_sent.is_set():
                    return {"type": "http.disconnect"}

                async with anyio.create_task_group() as task_group:

                    async def wrap(func: typing.Callable[[], typing.Awaitable[T]]) -> T:
                        result = await func()
                        task_group.cancel_scope.cancel()
                        return result

                    task_group.start_soon(wrap, response_sent.wait)
                    message = await wrap(request.receive)

                if response_sent.is_set():
                    return {"type": "http.disconnect"}

                return message

        async def close_recv_stream_on_response_sent() -> None:
            await response_sent.wait()
            recv_stream.close()

        async def send_no_error(message: Message) -> None:
                try:
                    await send_stream.send(message)
                except anyio.BrokenResourceError:
                    # recv_stream has been closed, i.e. response_sent has been set.
                    return

        async def coro() -> None:
                nonlocal app_exc

                async with send_stream:
                    try:
                        await self.app(scope, receive_or_disconnect, send_no_error)
                    except Exception as exc:
                        app_exc = exc

        task_group.start_soon(close_recv_stream_on_response_sent)
        task_group.start_soon(coro)


        try:
                message = await recv_stream.receive()
                info = message.get("info", None)
                if message["type"] == "http.response.debug" and info is not None:
                    message = await recv_stream.receive()
        except anyio.EndOfStream:
            if app_exc is not None:
                raise app_exc
            raise RuntimeError("No response returned.")

        async def call_next(status_code, content, raw_headers, use_response: bool = True) -> Response:
            if use_response:
                response = Response(
                    status_code=message["status"], content=content, headers=message["headers"]
                )
                return response
            else:
                return content, raw_headers

        async with anyio.create_task_group() as task_group:
            request = Request(scope, receive=receive)
            response = await self.dispatch_func(request, call_next)
            await response(scope, receive, send)
            response_sent.set()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        raise NotImplementedError()  # pragma: no cover