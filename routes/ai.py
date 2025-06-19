
# from fastapi import APIRouter, Depends


# openai.api_key = "YOUR_API_KEY"

# router = APIRouter(prefix="/ai", tags=["ai"])

# @router.post("/chat")
# async def chat_with_ai(prompt: str):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return {"response": response.choices[0].message.content}
#     except OpenAIError as e:
#         return {"error": str(e)}