from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI
from loguru import logger

from app.utils.auth import api_key_dependency
from app.model.model_schema import ActionResponse, Event
from app.model.recommender import DefaultRecommender
from app.utils.art import load_ascii_art
from settings import settings


CONFIG_PATH = Path(__file__).resolve().parent / "config" / "default.yaml"

recommender = DefaultRecommender(CONFIG_PATH)

@asynccontextmanager
async def lifespan(app: FastAPI):
    art = load_ascii_art()
    if art:
        logger.info("\n{}", art)
    yield


app = FastAPI(
    title="TARS Recommender Service",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post(
    "/recommend-action",
    response_model=ActionResponse,
    dependencies=[Depends(api_key_dependency)],
)
async def recommend_action(event: Event) -> ActionResponse:
    logger.info(
        "Processing recommendation request for event_id={} env={}",
        event.id,
        settings.env,
    )
    return recommender.recommend(event)
