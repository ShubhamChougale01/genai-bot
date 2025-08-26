import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from tools.Document_QAimport rag_chain
from tools.calculator import calculator_tool
from tools.web_search import web_search_tool
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="gemma2-9b-it", api_key=os.getenv("GROQ_API_KEY"))

pdf_qa_chain = rag_chain()

tools = [
    Tool(
        name="pdf_qa",
        func=lambda query: pdf_qa_chain.run(query),
        description="Use this to answer questions from the PDF document."
    ),
    Tool(
        name="calculator",
        func=calculator_tool,
        description="Use this to answer arithmetic questions."
    ),
    Tool(
        name="web_search",
        func=web_search_tool,
        description="Use this to search information on the web and always return answers in English only.."
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
    test_query = "What is Generative AI?"
    print("Query:", test_query)
    print("Response:", answer_query(test_query))
