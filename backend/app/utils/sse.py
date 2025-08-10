"""Utilities to generate server‑sent events for streaming responses."""

from fastapi.responses import StreamingResponse


def sse_event(data: str) -> bytes:
    """Format a single SSE data event."""
    return f"data: {data}\n\n".encode("utf-8")


def stream_tokens(generator):
    """
    Wrap a token generator into a StreamingResponse. Yields each token as
    an SSE event and finally sends an [END] marker.
    """

    def iter_stream():
        for token in generator:
            yield sse_event(token)
        yield sse_event("[END]")

    return StreamingResponse(iter_stream(), media_type="text/event-stream")