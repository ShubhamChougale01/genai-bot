import os
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor, Tool
from langchain.prompts import PromptTemplate
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

def pdf_tool_func(query: str) -> str:
    return pdf_qa_chain.invoke({"query": query})["result"]

def calculator_func(query: str) -> str:
    return calculator_tool(query)

def web_search_func(query: str) -> str:
    return web_search_tool(query)


tools = [
    Tool(
        name="pdf_qa",
        func=pdf_tool_func,
        description="Use the tool to answer questions about Generative AI concepts, challenges, or introductory topics from the genai_intro.pdf document."
    ),
    Tool(
        name="calculator",
        func=calculator_func,
        description="Use this tool to perform arithmetic operations."
    ),
    Tool(
        name="web_search",
        func=web_search_func,
        description="Use this to search information on the web and always return answers in English only."
    )
]

memory = ConversationBufferMemory(
    memory_key="chat_history",   
    return_messages=True       
)

prompt = PromptTemplate(
    input_variables=["input", "chat_history", "agent_scratchpad"],
    template="""
You are a helpful assistant with access to the tools: pdf_qa, calculator, web_search.

Chat history:  
{chat_history}
Instructions:
- When the user asks a question, think step by step.
- Decide which tool to call, if any.
- Use ONLY the tools listed above.
- If you use a tool, show your reasoning in the scratchpad, then provide the final answer.
- Always respond in English.
- Do NOT answer questions that do not involve the listed tools.
- Never provide personal information (e.g., email, phone number, or sensitive data).
 

Question: {input}
{agent_scratchpad}
"""
)

agent = create_tool_calling_agent(
    llm=llm, 
    tools=tools, 
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,   
    verbose=False,
)

def answer_query(query: str) -> str:
    try:
        result = agent_executor.invoke({"input": query})
        return result["output"] 
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
