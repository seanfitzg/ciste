from dotenv import load_dotenv
from langchain.agents import create_agent
from langsmith import uuid7

from ciste.context import Context
from ciste.tools.account_tools import get_account, list_transactions

load_dotenv()

agent = create_agent(
    model="openai:gpt-6.1-sol",
    tools=[get_account, list_transactions],
    system_prompt="You are a helpful assistant for a banking application. You have access to the following tools: get_account and list_transactions. Use these tools to assist the user with their banking needs.",
    context_schema=Context,
)


def test_invoke():
    config = {"configurable": {"thread_id": str(uuid7())}}
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What is my most recent transaction?"}
            ]
        },
        config=config,
        context=Context(customer_id="C001", tier="retail"),
    )
    result["messages"][-1].pretty_print()


# test_invoke()
