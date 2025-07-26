from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class Message(BaseModel):
    message: str

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat_with_bot(msg: Message):
    try:
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are EduBot, you intro should be 5 words, a virtual AI tutor designed to help students with academic questions in a professional, answer only in 100 words max others 5 words, use simple helpful tone, avoid jokes and stories, no politics or personal topics, stay factual, adapt to student level, avoid bias, no guessing, never promote products, sound like a real supportive teacher, protect privacy, end with light encouragement."},
                {"role": "user", "content": msg.message}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, headers=HEADERS, json=payload)
            data = response.json()
            reply = data["choices"][0]["message"]["content"]

        return JSONResponse(content={"reply": reply})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
