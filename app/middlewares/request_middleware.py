import time
import uuid
from fastapi import Request


async def request_middleware(request: Request, call_next):
    start_time = time.time()

    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())[:8]
    )

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    response.headers["X-Request-ID"] = request_id

    print(
        f"{request.method} {request.url.path} "
        f"Status:{response.status_code} "
        f"RequestID:{request_id}"
    )

    return response