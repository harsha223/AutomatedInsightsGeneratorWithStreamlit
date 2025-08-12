import os
import sys
import warnings
import streamlit as st
import unidecode
from helper import display_code_plots, display_text_with_images
from llm_agent import initialize_python_agent, initialize_sql_agent
from constants import USER, PASSWORD, OPENAI_API_KEY, LLM_MODEL_NAME, HOST, DATABASE, PORT

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.insert(0, parent_dir)

# Set environment variables
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Configure Streamlit page
st.set_page_config(page_title="Data Insights")

# Initialize session state
if 'agent_memory' not in st.session_state:
    st.session_state['agent_memory_sql'] = initialize_sql_agent()
    st.session_state['agent_memory_python'] = initialize_python_agent()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    st.session_state.sql_agent = st.session_state['agent_memory_sql']
    st.session_state.python_agent = st.session_state['agent_memory_python']


def generate_response(code_type, input_text):
    """
    Generate a response based on the provided input text and code type.

    Args:
        code_type (str): The type of code to be generated ("python" or "sql").
        input_text (str): The input text to be processed.

    Returns:
        str: The generated response based on the input text and code type.
             If no response is generated, it returns "NO_RESPONSE".
    """
    local_prompt = unidecode.unidecode(input_text)
    if code_type == "python":
        try:
            local_response = st.session_state.sql_agent.invoke({"input": local_prompt})['output']
            print("Response->", local_response)
        except:
            return "NO_RESPONSE"
        exclusion_keywords = ["please provide", "don't know", "more context", "provide more", "vague request"]
        if any(keyword in local_response.lower() for keyword in exclusion_keywords):
            return "NO_RESPONSE"
        local_prompt = {"input": "Write a code in python to plot the following data\n\n" + local_response}
        return st.session_state.python_agent.invoke(local_prompt)
    else:
        return st.session_state.sql_agent.run(local_prompt)


def reset_conversation():
    st.session_state.messages = []
    st.session_state.sql_agent = initialize_sql_agent()
    st.session_state.python_agent = initialize_python_agent()


# Display title and reset button
st.title("Data Insights")
col1, col2 = st.columns([3, 1])
with col2:
    st.button("Reset Chat", on_click=reset_conversation)

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] in ("assistant", "error"):
            display_text_with_images(message["content"])
        elif message["role"] == "plot":
            exec(message["content"])
        else:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Please ask your question:"):
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    keywords = ["plot", "graph", "chart", "diagram"]
    if any(keyword in prompt.lower() for keyword in keywords):
        prev_context = ""
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "assistant":
                prev_context = msg["content"] + "\n\n" + prev_context
                break
        if prev_context:
            prompt += f"\n\nGiven previous agent responses:\n{prev_context}\n"
        response = generate_response("python", prompt)
        if response == "NO_RESPONSE":
            response = "Please try again with a re-phrased query and more context"
            with st.chat_message("error"):
                display_text_with_images(response)
            st.session_state.messages.append({"role": "error", "content": response})
        else:
            code = display_code_plots(response['output'])
            try:
                code = f"import pandas as pd\n{code.replace('fig.show()', '')}"
                code += "st.plotly_chart(fig, theme='streamlit', use_container_width=True)"
                exec(code)
                st.session_state.messages.append({"role": "plot", "content": code})
            except:
                response = "Please try again with a re-phrased query and more context"
                with st.chat_message("error"):
                    display_text_with_images(response)
                st.session_state.messages.append({"role": "error", "content": response})
    else:
        if len(st.session_state.messages) > 1:
            context_length = 0
            prev_context = ""
            for msg in reversed(st.session_state.messages):
                if context_length > 1:
                    break
                if msg["role"] == "assistant":
                    prev_context = msg["content"] + "\n\n" + prev_context
                    context_length += 1
            response = generate_response("sql", f"{prompt}\n\nGiven previous agent responses:\n{prev_context}\n")
        else:
            response = generate_response("sql", prompt)
        with st.chat_message("assistant"):
            display_text_with_images(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
