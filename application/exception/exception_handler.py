from starlette.responses import JSONResponse


async def handle_api_exceptions(request, exc):
    _ = request
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"status": exc.status_code, "detail": exc.message}
                 })
