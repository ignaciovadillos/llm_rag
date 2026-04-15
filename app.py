import streamlit as st
from rag import load_collection, ask_owl
import ollama

st.set_page_config(
    page_title="The Know-It Owl",
    page_icon="🦉"
)

st.title("🦉 The Know-It Owl")
st.caption("An enchanted owl of extraordinary erudition.")

# Load collection once
@st.cache_resource
def get_collection():
    return load_collection("owl_db")

collection = get_collection()

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask the owl about the Wizarding World..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # 🔥 RAG retrieval first
        answer, sources = ask_owl(
            query=prompt,
            collection=collection,
            history=st.session_state.history
        )

        # 🔥 STREAMING (simulate token flow)
        for token in answer.split():
            full_response += token + " "
            placeholder.markdown(full_response + "▌")

        # Build sources block
        seen = set()
        citations = []

        for _, meta, _ in sources:
            key = (meta["book"], meta["chapter_number"])
            if key not in seen:
                seen.add(key)
                citations.append(
                    f"- **{meta['book']}**, Chapter {meta['chapter_number']}: {meta['chapter_title']}"
                )

        if citations:
            full_response += "\n\n**Sources consulted:**\n" + "\n".join(citations)

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

# Sidebar
with st.sidebar:
    st.header("Settings")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun