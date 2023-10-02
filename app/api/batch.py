
from fastapi import APIRouter, BackgroundTasks
from app.services import batch_service, abstractive_service, notice_service


router = APIRouter()


@router.post('/scrap/{type}/start', name='batch:scrap:start')
async def start(type: str, background_tasks: BackgroundTasks):
    type = type.replace('-', '_').upper()
    background_tasks.add_task(batch_service.start_batch, type)
    return {"result": "success"}


@router.post('/notice/start', name='batch:notice:start')
async def notice_geek(param: notice_service.NoticeReq, background_tasks: BackgroundTasks):
    background_tasks.add_task(notice_service.exec, param)
    return {"result": "success"}


@router.post('/reabstractive', name='batch:reabstractive')
async def reabstractive(param: abstractive_service.ReabstractiveReq):
    await abstractive_service.reabstractive(param)
    return {"result": "success"}


@router.post('/reabstractive-all-empty', name='batch:reabstractive')
async def reabstractive_all_empty(background_tasks: BackgroundTasks):
    background_tasks.add_task(abstractive_service.reabstractive_emptys)
    return {"result": "success"}
