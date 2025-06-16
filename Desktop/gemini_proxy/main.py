from fastapi import FastAPI, Request
import httpx
import os
import datetime

app = FastAPI()

# Real Gemini API key here
REAL_GEMINI_API_KEY = "AIzaSyDyc0VPf0bK-MBURytMDqdBdM9Gj9EA7gQ"

@app.post("/v1beta/models/gemini-pro-vision:generateContent")
async def proxy(request: Request):
    data = await request.json()

    # Try to log the prompt text
    try:
        parts = data["contents"][0]["parts"]
        prompt_text = next((part["text"] for part in parts if "text" in part), "NO TEXT")
        with open("prompt_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.datetime.now()} | Prompt: {prompt_text}\n")
    except Exception as e:
        print("Failed to log:", e)

    # Forward to Gemini
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={REAL_GEMINI_API_KEY}",
            json=data,
            headers=headers
        )
    return res.json()
