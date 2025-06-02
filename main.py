from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
from db import insert_url, get_url_by_code, get_code_by_long_url
from datetime import datetime
import random, string
from redis_client import get_redis_client
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()  # 預設會讀取 .env 檔

app = FastAPI()

# 加上 CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://frontend-url-shortener-2v980dtzs-hungshengs-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post('/shorten')
def shortern_url(long_url: str = Form(...)):
    cached_code = redis_client.get(f"longurl:{long_url}")
    if cached_code:
        return {"short_url": f"http://localhost:8000/{cached_code}"}
    existing_code = get_code_by_long_url(long_url)
    if existing_code:
        redis_client.set(f"longurl:{long_url}", existing_code, ex=60*60)
        redis_client.set(existing_code, long_url, ex=60*60)
        return {"short_url": f"http://localhost:8000/{existing_code}"}
    
    for _ in range(5):  # 最多嘗試 5 次
        short_code = generate_short_code()
        if not get_url_by_code(short_code):
            break

    try:
        insert_url(long_url, short_code)
        return {"short_url": f"http://localhost:8000/{short_code}", }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

redis_client = get_redis_client()


@app.get("/{code}")
def direct_url(code: str):
    cached_url = redis_client.get(code)
    if cached_url:
        return RedirectResponse(cached_url)
    
    long_url = get_url_by_code(code)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    redis_client.set(code, long_url, ex=60*60)
    redis_client.set(f"longurl:{long_url}", code, ex=60*60)
    
    return RedirectResponse(long_url)





