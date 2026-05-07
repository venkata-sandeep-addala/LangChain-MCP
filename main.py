import asyncio

from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

llm = ChatGroq(model="llama-3.3-70b-versatile")

stdio_server_params = StdioServerParameters(
    command="Python", args=["D:\\Projects\\LangChain-MCP\\servers\\math_server.py"]
)


async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session Intialized")
            
            tools = await load_mcp_tools(session)
            print("\n\n")
            
            agent = create_agent(llm, tools)
            
            response = await agent.ainvoke({"messages": [HumanMessage(content="what is 54+ 3 * 2?")]})
            print(response['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
