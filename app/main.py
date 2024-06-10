import os
from typing import List

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from .routers import manga, ranobe

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(manga.router)
app.include_router(ranobe.router)

@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_form(request: Request, text_input: str = Form(...)):
    processed_lines = []
    lines = text_input.split("\n")
    for line in lines:
        line = line.strip().replace('\r', '')
        if line:
            slug = line.split("/")
            try: # Добавляем блок try...except для обработки исключений
                if slug[-1] in ['chapters', 'comments', 'statistics', ' ', '', '/']:
                    processed_lines.append(f"http://bypass.mwx.su/manga/{slug[-2]}")
                else:
                    processed_lines.append(f"http://bypass.mwx.su/manga/{slug[-1]}")
            except IndexError: # Ловим исключение, если slug пустой
                print(f"Ошибка обработки строки: '{line}'") 
                processed_lines.append(f"Ошибка обработки: {line}")
        else:
            print("Пропущена пустая строка")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "lines": lines, "processed_lines": processed_lines},
    )
    
    
@app.post("/download")
async def download_file(request: Request, processed_lines: List[str] = Form(...)):
    output = "\n".join(processed_lines)
    with open("output.txt", "w") as f:
        f.write(output)
    return FileResponse("output.txt", filename="processed_text.txt")