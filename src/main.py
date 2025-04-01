from fastapi import FastAPI
from src.api.peaks import router as peaks_router
from dotenv import load_dotenv
import os
import sentry_sdk

# Load environment variables
load_dotenv()
IS_PRODUCTION = os.getenv("PRODUCTION", "FALSE").lower() == "true"

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profile_session_sample_rate=1.0,
    # Set profile_lifecycle to "trace" to automatically
    # run the profiler on when there is an active transaction
    profile_lifecycle="trace",
)

app = FastAPI(
    title="Peaks API",
    description="Find data about mountains.",
    version="1.0",
    docs_url=None if IS_PRODUCTION else "/docs",  # Disable Swagger UI
    redoc_url=None if IS_PRODUCTION else "/redoc",  # Disable ReDoc
    openapi_url=None if IS_PRODUCTION else "/openapi.json"
)
app.include_router(peaks_router)


# @app.get("/")
# def read_root():
#     return