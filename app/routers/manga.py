from fastapi import APIRouter
from app.services.manga import senkuro

router = APIRouter()


@router.get("/manga/{site_name}/search/")
async def search_manga(site_name: str, text: str):
    if site_name == 'senkuro':
        return await senkuro.search_manga(text)


@router.get("/manga/{site_name}/title/{slug}")
@router.get("/manga/{slug}")
async def info_title(slug: str, site_name: str = 'senkuro'):
    if site_name == 'senkuro':
        return await senkuro.info_title(slug)
    

@router.get("/manga/{site_name}/chapters/{slug}")
async def chapters_title(site_name: str, slug: str):
    if site_name == 'senkuro':
        response = await senkuro.chapters_title(slug)
        return response
    
@router.get("/manga/{site_name}/images/{slug}/{chapterId}")
async def images_title(site_name: str, slug: str, chapterId: str):
    if site_name == 'senkuro':
        return await senkuro.images_title(slug, chapterId)
