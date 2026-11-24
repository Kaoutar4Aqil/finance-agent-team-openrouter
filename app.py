import streamlit as st
import uuid

from finance_agent_team import build_team

st.set_page_config(
    page_title="Finance AI Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Finance AI Assistant")
st.caption("Multi-Agent Intelligence • Agno • OpenRouter")

with st.sidebar:
    st.header("AI Agent Team")

    st.info("🌐 Web Research Agent")
    st.success("📈 Financial Data Agent")
    st.info("🧠 Team Coordinator")

    st.divider()

    if st.button("New conversation"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.pop("team", None)
        st.rerun()

    st.caption(
        "Educational purposes only. "
        "Not financial advice."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "team" not in st.session_state:
    try:
        st.session_state.team = build_team()
    except Exception:
        st.error(
            "Unable to initialize the agents. "
            "Check your API configuration."
        )
        st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask me anything about financial markets..."
)

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI agents are working..."):
            try:
                response = st.session_state.team.run(
                    prompt,
                    session_id=st.session_state.session_id
                )

                answer = str(response.content)
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception:
                st.error(
                    "Unable to complete the request. "
                    "Please try again."
                )
