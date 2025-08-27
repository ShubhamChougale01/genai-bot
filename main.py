import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from tools.Document_QA import rag_chain
from tools.calculator import calculator_tool
from tools.web_search import web_search_tool

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="gemma2-9b-it", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
    )

pdf_qa_chain = rag_chain()

tools = [
    Tool(
        name="pdf_qa",
        func=lambda query: pdf_qa_chain.invoke({"query": query})["result"],
        description="Use the tool to answer questions about Generative AI concepts, challenges, or introductory topics from the genai_intro.pdf document."
    ),
    Tool(
        name="calculator",
        func=calculator_tool,
        description="Use this tool to perform arithmetic operations."
    ),
    Tool(
        name="web_search",
        func=web_search_tool,
        description="Use this to search information on the web and always return answers in English only."
    )
]

memory = ConversationBufferMemory(
    memory_key="chat_history",   
    return_messages=True       
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)


def answer_query(query: str) -> str:
    try:
        return agent.run(query)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    test_queries = [
        "What is Generative AI?",
        "List one challenge of GenAI.",
        "What is 45 × 19?",
        "Who is the Prime Minister of India?"
    ]
    for query in test_queries:
        print("\n---")
        print("Query:", query)
        print("Response:", answer_query(query))
