master_template = """
Answer the following questions as best you can. 

You are in the middle of a conversation. The chat history is the following:

{chat_history}

You have access to the following user-configurated variables:

{user_configurated_variables}

You have access to the following tools:

{tools}

ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought -> Action + Action Input -> Observation can repeat N times)

Final Answer: the final answer to the original input question. This Final Answer, have a format based on the tool you used. The possible formats which depend on the tool that you are using are
{tools_final_answer_formats}

Question: {input}
{agent_scratchpad}
"""
