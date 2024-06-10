from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.ranobe import ranobe_me, ranobehub, ranobelib, ranobepoisk, ranobes
from urllib.parse import urlparse


router = APIRouter()


@router.get('/ranobe/download/')
async def ranobe_download(href: str):
    if not href:
        return {"error": "Missing 'href' parameter"}

    parsed_url = urlparse(href)
    domain = parsed_url.netloc
    if 'ranobe.me' == domain:
        fb2_content = await ranobe_me.download(href)
    elif 'ranobehub.org' == domain:
        fb2_content = await ranobehub.download(href)
    elif 'ranobelib.org' == domain:
        fb2_content = await ranobelib.download(href)
    elif 'ranobepoisk.ru' == domain:
        fb2_content = await ranobepoisk.download(href)
    elif 'ranobes.com' == domain:
        fb2_content = await ranobes.download(href)
    if fb2_content:
        with open("ranobe.fb2", "wb") as f:
            f.write(fb2_content.encode('utf-8'))

        return FileResponse("ranobe.fb2",
                            media_type='application/xml',
                            filename="ranobe.fb2")
    else:
        return {"error": f"Failed to download '{href}'"}
