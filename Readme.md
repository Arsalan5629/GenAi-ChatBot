# ChatBot AI

A chatbot application built with Streamlit, LangChain, and Mistral AI, with persistent conversation history stored in PostgreSQL.

![ChatBot AI interface](assets/ChatBot.png)

## Features

- Real-time chat interface powered by Mistral's `mistral-small` model
- Multiple conversations with a sidebar chat history list
- Create new chats and switch between existing ones
- Delete conversations with an inline confirmation prompt
- Collapsible sidebar with a show/hide toggle
- Auto-generated chat titles based on the first message in a conversation
- Conversations and messages persisted in PostgreSQL, so history survives restarts
- Custom dark-themed interface built on top of Streamlit

## Tech Stack

- Frontend/App Framework: Streamlit
- LLM Orchestration: LangChain
- Model Provider: Mistral AI (`langchain-mistralai`)
- Database: PostgreSQL
- Language: Python

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── crud.py             # Database operations (create, read, update, delete chats/messages)
├── assets/              # Screenshots and static assets
├── .env                 # Environment variables (not committed)
├── requirements.txt    # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- A PostgreSQL database (local or hosted)
- A Mistral AI API key

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/Arsalan5629/GenAi-ChatBot.git
   cd GenAi-ChatBot
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your credentials

   ```env
   MISTRAL_API_KEY=your_mistral_api_key
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

5. Run the application

   ```bash
   streamlit run app.py
   ```

6. Open the application in your browser at `http://localhost:8501`

## Usage

- Click "New Chat" in the sidebar to start a fresh conversation.
- Click any conversation in the sidebar to switch to it; the full message history loads automatically.
- Use the delete icon next to a chat to remove it, with a confirmation step before deletion.
- Use the toggle button at the top of the page to show or hide the sidebar.
- Type a message in the input box at the bottom and press Enter to chat with the assistant.

## Roadmap

- Streaming responses token-by-token
- User authentication for multi-user support
- Editable/renamable chat titles
- Export conversation history

## Author

Made by Arsalan

## License

This project is open source and available under the [MIT License](LICENSE).