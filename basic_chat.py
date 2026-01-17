from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # change to gemini-2.0-flash or gemini-1.5-flash if needed
    temperature=0
)

# Messages (same structure as ChatOpenAI)
messages = [
    ("system", "You are a helpful assistant that identifies fake news in the presented content"),
    ("human", "cats now speak fluent english!"),
]

# Invoke the model
ai_msg = llm.invoke(messages)

# Print result
print(ai_msg.content)
