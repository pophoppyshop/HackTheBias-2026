from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage 


def identify_fake_news(llm_model, text_input: str) -> str:
    messages = [
        SystemMessage(content="""You are a fake news classifier.
Always respond in the following format exactly:

is_fake_news: <true|false>
justification: <short explanation>"""),
        HumanMessage(content=text_input)
    ]

    # Use .generate() instead of calling the object
    result = llm_model.generate([messages])
    
    # The generated text is inside result.generations[0][0].text
    return result.generations[0][0].text

class Text_Query(BaseModel):
    Title: str
    Content: str


llm_gemini = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

app = FastAPI()

@app.post("/items/")
async def create_item(query: Text_Query):
    output_msg = identify_fake_news(llm_gemini, query.Content)
    return {"title": query.Title, "result": output_msg}
