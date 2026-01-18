from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # change to gemini-2.0-flash or gemini-1.5-flash if needed
    temperature=0
)

# Messages (with structured output)
messages = [
    (
        "system",
        """You are a fake news classifier.
Always respond in the following format exactly:

is_fake_news: <true|false>
justification: <short explanation>
"""
    ),
    ("human", "cats now speak fluent english!")
]


# Invoke the model
ai_msg = llm.invoke(messages)

# Print result
print(ai_msg.content)
