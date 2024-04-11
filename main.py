import starlette.status as status
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config import server_config
from routes import users

server = FastAPI()
# user routes
server.include_router(
    users,
    prefix=server_config.CURRENT_API_URL,
)


@server.get("/")
async def root():
    """
    Redirects incoming GET requests to the API documentation page.
    """

    # Redirecting to the API documentation page using a 302 status code
    return RedirectResponse(
        url="/docs",
        status_code=status.HTTP_302_FOUND,
    )
