import streamlit as st

from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from crud import (
    create_chat,
    delete_chat,
    get_all_chats,
    get_messages,
    save_message,
    update_chat_title
)


load_dotenv()


st.set_page_config(
    page_title="Arsalan AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True

if "chat_id" not in st.session_state:
    chats = get_all_chats()
    if chats:
        st.session_state.chat_id = chats[0].id
    else:
        st.session_state.chat_id = create_chat()

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None


base_css = """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: #0b0f19;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
    transition: margin-left 0.25s ease-in-out;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

.brand {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 4px 18px 4px;
}

.brand-text {
    display: flex;
    flex-direction: column;
}

.brand-title {
    font-size: 22px;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 2px;
}

.brand-subtitle {
    font-size: 12px;
    color: #9ca3af;
}

.hero {
    text-align: center;
    padding: 45px 20px 30px 20px;
}

.hero-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 34px;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 8px;
}

.hero-description {
    font-size: 15px;
    color: #9ca3af;
}

.chat-container {
    max-width: 850px;
    margin: auto;
}

.stChatMessage {
    background: transparent;
    border: none;
    padding: 8px 0;
}

[data-testid="stChatMessageContent"] {
    border-radius: 16px;
    padding: 12px 16px;
}

[data-testid="stChatInput"] {
    max-width: 850px;
    margin: auto;
}

.sidebar-section {
    font-size: 11px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 18px 0 8px 6px;
}

.info-card {
    background: #182131;
    border: 1px solid #263244;
    border-radius: 12px;
    padding: 12px;
    margin-top: 15px;
}

.info-title {
    color: #f3f4f6;
    font-size: 13px;
    font-weight: 600;
}

.info-text {
    color: #9ca3af;
    font-size: 12px;
    margin-top: 4px;
}

.footer-text {
    text-align: center;
    color: #4b5563;
    font-size: 12px;
    margin-top: 30px;
    padding-bottom: 20px;
}

div[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent;
    border: 1px solid transparent;
    text-align: left;
    color: #d1d5db;
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

div[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: #1c2536;
    border: 1px solid #263244;
    color: #f9fafb;
}

.chat-row-active button[kind="secondary"] {
    background: #1e293b;
    border: 1px solid #334155;
    color: #f9fafb;
    font-weight: 600;
}

.toggle-btn button {
    background: #182131;
    border: 1px solid #263244;
    color: #d1d5db;
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 14px;
}

.toggle-btn button:hover {
    background: #1c2536;
    color: #f9fafb;
}

</style>
"""

st.markdown(base_css, unsafe_allow_html=True)

if st.session_state.sidebar_visible:
    sidebar_toggle_css = """
    <style>
    [data-testid="stSidebar"] {
        margin-left: 0px;
    }
    </style>
    """
else:
    sidebar_toggle_css = """
    <style>
    section[data-testid="stSidebar"] {
        width: 0px !important;
        min-width: 0px !important;
        max-width: 0px !important;
        overflow: hidden !important;
        margin-left: -1px;
    }
    section[data-testid="stSidebar"] > div {
        width: 0px !important;
        min-width: 0px !important;
    }
    div[data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    </style>
    """

st.markdown(sidebar_toggle_css, unsafe_allow_html=True)


@st.cache_resource
def get_model():
    return ChatMistralAI(
        model_name="mistral-small-2506"
    )


model = get_model()


toggle_col, _ = st.columns([1, 20])

with toggle_col:
    toggle_label = "☰" if not st.session_state.sidebar_visible else "«"
    if st.button(toggle_label, key="sidebar_toggle", help="Show/hide sidebar"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()


with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-text">
                <div class="brand-title">🤖 Arsalan AI</div>
                <div class="brand-subtitle">Mistral-powered assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("＋  New Chat", use_container_width=True):
        st.session_state.chat_id = create_chat()
        st.rerun()

    st.markdown('<div class="sidebar-section">Conversations</div>', unsafe_allow_html=True)

    chats = get_all_chats()

    for chat in chats:

        is_active = chat.id == st.session_state.chat_id
        row_class = "chat-row-active" if is_active else "chat-row"

        st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)

        title_col, delete_col = st.columns([5, 1])

        with title_col:
            if st.button(
                chat.title or "New Chat",
                key=f"chat_{chat.id}",
                use_container_width=True
            ):
                st.session_state.chat_id = chat.id
                st.session_state.confirm_delete = None
                st.rerun()

        with delete_col:
            if st.button("🗑️", key=f"delete_{chat.id}"):
                st.session_state.confirm_delete = chat.id
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.confirm_delete == chat.id:
            st.warning(f"Delete '{chat.title or 'New Chat'}'?")
            confirm_col, cancel_col = st.columns(2)
            with confirm_col:
                if st.button("Delete", key=f"confirm_{chat.id}", use_container_width=True):
                    delete_chat(chat.id)
                    st.session_state.confirm_delete = None
                    remaining = get_all_chats()
                    if remaining:
                        st.session_state.chat_id = remaining[0].id
                    else:
                        st.session_state.chat_id = create_chat()
                    st.rerun()
            with cancel_col:
                if st.button("Cancel", key=f"cancel_{chat.id}", use_container_width=True):
                    st.session_state.confirm_delete = None
                    st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">⚡ Mistral Small</div>
            <div class="info-text">
                Fast AI responses powered by Mistral.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">🗄️ PostgreSQL</div>
            <div class="info-text">
                Your conversations are securely stored in your database.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer-text">
            Built with Streamlit + LangChain<br>
            Made by Arsalan
        </div>
        """,
        unsafe_allow_html=True
    )


messages = get_messages(st.session_state.chat_id)


if not messages:

    st.markdown(
        """
        <div class="hero">
            <div class="hero-icon">🤖</div>
            <div class="hero-title">How can I help you?</div>
            <div class="hero-description">
                Ask me anything and start a conversation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


conversation = [
    SystemMessage(
        content=(
            "You are a helpful, intelligent and friendly AI assistant. "
            "Give clear, accurate and useful answers."
        )
    )
]


for message in messages:

    if message.role == "user":

        conversation.append(HumanMessage(content=message.content))

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(message.content)

    elif message.role == "assistant":

        conversation.append(AIMessage(content=message.content))

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message.content)


if prompt := st.chat_input("Message Arsalan AI..."):

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    save_message(
        chat_id=st.session_state.chat_id,
        role="user",
        content=prompt
    )

    existing_messages = get_messages(st.session_state.chat_id)

    if len(existing_messages) == 1:

        title = prompt.strip()

        if len(title) > 40:
            title = title[:40] + "..."

        update_chat_title(st.session_state.chat_id, title)

    conversation.append(HumanMessage(content=prompt))

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            response = model.invoke(conversation)
            response_text = response.content

        st.markdown(response_text)

    save_message(
        chat_id=st.session_state.chat_id,
        role="assistant",
        content=response_text
    )

    st.rerun()