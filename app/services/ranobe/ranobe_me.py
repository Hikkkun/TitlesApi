import aiohttp
from bs4 import BeautifulSoup

from app.utils.f2b_creater.f2b import FB2Builder


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()

    soup = BeautifulSoup(response, 'html.parser')
    
    title = soup.select_one('div.MessageAloneHead a').text
    header = soup.select_one('div.ReadTextContainerIn h1').text
    
    paragraphs = [p for p in soup.find_all('p', {'class': 'fict'})]
    
    fb2 = FB2Builder(title)
    chapter = fb2.add_section(header)
    
    for index, paragraph in enumerate(paragraphs):
        if index != 0:
            fb2.add_paragraph(chapter, paragraph.text)
            fb2.add_empty_line(chapter)
    
    content = fb2.generate()
    
    return content