# Copyright (c) 2024, Nyrkiö Oy

from typing import Dict, List, Optional, Any, Union
from backend.core.core import (
    PerformanceTestResult,
    PerformanceTestResultSeries,
    ResultMetric,
)

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, RootModel

from backend.auth import auth
from backend.db.db import User, DBStore

app = FastAPI(openapi_url="/openapi.json")


api_router = APIRouter()


@api_router.get("/results")
async def results(user: User = Depends(auth.current_active_user)) -> List[Dict]:
    store = DBStore()
    results = await store.get_test_names(user)
    return [{"test_name": name} for name in results]


@api_router.delete("/results")
async def delete_results(user: User = Depends(auth.current_active_user)) -> List:
    store = DBStore()
    await store.delete_all_results(user)
    return []


@api_router.get("/result/{test_name}")
async def get_result(
    test_name: str, user: User = Depends(auth.current_active_user)
) -> List[Dict]:
    store = DBStore()
    test_names = await store.get_test_names(user)

    if not list(filter(lambda name: name == test_name, test_names)):
        raise HTTPException(status_code=404, detail="Not Found")

    return await store.get_results(user, test_name)


@api_router.delete("/result/{test_name}")
async def delete_result(
    test_name: str,
    timestamp: Union[int, None] = None,
    user: User = Depends(auth.current_active_user),
) -> List[Dict]:
    store = DBStore()
    test_names = await store.get_test_names(user)

    if not list(filter(lambda name: name == test_name, test_names)):
        raise HTTPException(status_code=404, detail="Not Found")

    await store.delete_result(user, test_name, timestamp)
    return []


class TestResult(BaseModel):
    timestamp: int
    metrics: Optional[List[Dict]]
    attributes: Optional[Dict]


class TestResults(RootModel[Any]):
    root: List[TestResult]


@api_router.post("/result/{test_name}")
async def add_result(
    test_name: str, data: TestResults, user: User = Depends(auth.current_active_user)
):
    store = DBStore()
    await store.add_results(user, test_name, data.root)
    return {}


@api_router.get("/result/{test_name}/changes")
async def changes(test_name: str, user: User = Depends(auth.current_active_user)):
    store = DBStore()
    results = await store.get_results(user, test_name)
    series = PerformanceTestResultSeries(test_name)

    # TODO(matt) - iterating like this is silly, we should just be able to pass
    # the results in batch.
    for r in results:
        metrics = [
            ResultMetric(name=r["name"], unit=r["unit"], value=r["value"])
            for r in r["metrics"]
        ]
        result = PerformanceTestResult(
            timestamp=r["timestamp"], metrics=metrics, attributes=r["attributes"]
        )
        series.add_result(result)

    return await series.calculate_changes()


# Must come at the end, once we've setup all the routes
app.include_router(api_router, prefix="/api/v0")
app.include_router(auth.auth_router, prefix="/api/v0")


@app.on_event("startup")
async def do_db():
    from backend.db.db import do_on_startup

    await do_on_startup()
