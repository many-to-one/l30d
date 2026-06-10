from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routers.last30days import router as last30days_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="My Last30Days API")

# ============================
# STATIC
# ============================


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(last30days_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # return templates.TemplateResponse("main.html", {"request": request})
    return templates.TemplateResponse(
        request=request,
        name="main.html",
        context={
            "request": request,
            # "is_authenticated": bool(user),
            # "is_admin": bool(user and user.is_admin),
            # "user": user
        }
    )