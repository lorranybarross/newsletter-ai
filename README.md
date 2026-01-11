# Newsletter AI Agent (LangGraph + RAG) 🚀

Este é um agente inteligente que automatiza a criação de newsletters temáticas. Ele utiliza um **Grafo de Estados (LangGraph)** para garantir que a pesquisa de notícias sempre preceda a redação, além de possuir um **Cache Semântico (ChromaDB)** para evitar buscas duplicadas.

## ✨ Funcionalidades
- **Busca Inteligente**: Integração com Tavily para notícias em tempo real.
- **Cache Semântico**: Uso de Embeddings do Google para armazenar pesquisas por 24h no ChromaDB.
- **Workflow Controlado**: Fluxo garantido via LangGraph (Busca -> Filtro -> Escrita).
- **Exportação Profissional**: Geração de newsletter em formato PDF.

## 🛠️ Tecnologias
- **LLM:** Gemini 2.5 Flash
- **Framework:** LangChain & LangGraph
- **Vector Database:** ChromaDB
- **Busca:** Tavily API

## 🚀 Como Iniciar

1. **Clone o repositório:**
   ```bash
   git clone <seu-repositorio>
   cd newsletter-ai

