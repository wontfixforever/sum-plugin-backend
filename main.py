from fastapi import FastAPI, Request
import openai
import base64
import os

app = FastAPI()

# Use your OpenAI API key from environment variable or hard-code it temporarily (not recommended for production)
openai.api_key = os.getenv("OPENAI_API_KEY", "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")  # Replace with your key or set env var

@app.post("/sum-numbers")
async def sum_numbers(request: Request):
    data = await request.json()
    image_b64 = data["image"]
    image_data_url = f"data:image/png;base64,{image_b64}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": "Sum all numbers visible in this image. Return only the sum." },
                        { "type": "image_url", "image_url": { "url": image_data_url } }
                    ]
                }
            ],
            max_tokens=50
        )

        reply = response.choices[0].message.content.strip()
        return { "sum": reply }

    except Exception as e:
        return { "error": str(e) }
