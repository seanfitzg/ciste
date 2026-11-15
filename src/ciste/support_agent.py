from langchain.agents import create_agent

from ciste.context import Context
from ciste.tools.account_tools import get_account, list_transactions

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_account, list_transactions],
    system_prompt="You are a helpful assistant",
    context_schema=Context,
)
