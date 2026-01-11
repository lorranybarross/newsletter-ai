# 📰 AI-Driven Smart Newsletter Agent

An advanced AI Engineering project that automates news gathering and newsletter drafting using a **RAG (Retrieval-Augmented Generation)** architecture. This agent uses **LangGraph** to coordinate a deterministic workflow and **ChromaDB** for semantic caching to optimize API costs and performance.

## 🚀 Key Features

* **Deterministic Workflow**: Built with **LangGraph** to ensure the agent follows a strict pipeline: Search -> Filter -> Write.
* **Semantic Cache**: Uses **Google Gemini Embeddings** and **ChromaDB** to store search results. If a similar topic was researched within the last 24 hours, it retrieves data locally instead of calling the search API.
* **Real-time Intelligence**: Integrated with **Tavily Search API** for deep, up-to-date web research.
* **Smart Filtering**: Uses a dedicated LLM chain with **Pydantic** to select and summarize the top 3 most relevant news items.
* **Professional Output**: Automatically generates a structured Markdown newsletter and exports it to a **PDF**.

## 📂 Project Structure

```text
newsletter-ai/
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
├── .env                    # API Keys (Google, Tavily)
└── src/
    ├── __init__.py         # Package initializer
    ├── agents/             # LangGraph state machine logic
    ├── core/               # LLM and Embedding configurations
    ├── models/             # Data schemas and Pydantic models
    ├── templates/          # Prompt engineering and LLM chains
    ├── tools/              # Search tools and Vector DB logic
    └── utils/              # PDF Exporting and helper functions
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/youruser/newsletter-ai.git](https://github.com/youruser/newsletter-ai.git)
   cd newsletter-ai
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Configure Environment Variables: Create a `.env` file in the root directory:**
   ```bash
   GOOGLE_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key

## 🖥️ Usage

Run the main script to start the workflow:

```bash
python main.py
```

The agent follows these steps:
* **Semantic Check:** Consults the local ChromaDB for similar recent topics.
* **Web Research:** If no recent cache exists, it searches the web via Tavily.
* **Synthesis:** Filters findings and generates a cohesive narrative.
* **Export:** Saves the final newsletter as a PDF in the project root.

## 🧠 Technical Architecture

This project follows modern AI Engineering principles:
* **State Management:** Uses `TypedDict` to pass context and search results between nodes in the graph.
* **Separation of Concerns:** Decouples prompt logic from tool execution and model configuration.
* **Efficiency:** Reduces LLM hallucination by forcing the model to use retrieved search results as the only source of truth.
* **Persistence:** Implements a vector-based memory to ensure data durability and cost-efficiency.
