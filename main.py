from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage 

# Initialize FastAPI
app = FastAPI()

# ⚡ CORS settings for deployed app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming data
class Text_Query(BaseModel):
    Title: str
    Content: str

# Initialize Gemini LLM
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Fake news classifier function
def identify_fake_news(llm_model, text_input: str) -> str:
    messages = [
        SystemMessage(content="""You are a fake news classifier.
Always respond in the following format exactly:

is_fake_news: <true|false>
justification: <short explanation>"""),
        HumanMessage(content=text_input)
    ]

    result = llm_model.generate([messages])
    return result.generations[0][0].text

# API route
@app.post("/items/")
async def create_item(query: Text_Query):
    output_msg = identify_fake_news(llm_gemini, query.Content)
    return {"title": query.Title, "result": output_msg}
