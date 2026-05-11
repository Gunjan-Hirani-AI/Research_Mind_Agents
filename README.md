# 🧠 Research Mind — Multi-Agent Research Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.2-green?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.35-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-black?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

> **Research Mind** is a production-grade multi-agent AI system designed to automate deep research. It doesn't just answer questions; it **thinks, searches, reads, and writes** autonomously by orchestrating a team of specialized agents.

---

## 🚀 Overview 
In this Project, I made Multi-Agent Research Assistant, which is a fully autonomous AI system that thinks, searches, reads and writes on its own.

Instead of a single AI answering your question from memory, we are deploying a team of specialized intelligent agents that collaborate together to produce a professional research report on any topic you give them.

The Search Agent goes out on the live internet and finds the most relevant and recent sources.

The Reader Agent then dives deep into those sources, scraping and extracting meaningful content.

The Writer Agent takes all that gathered intelligence and crafts a well-structured, detailed report.

And finally the Critic Agent reviews the entire report, scores it and gives feedback just like a senior researcher reviewing a junior's work.

Every single agent is powered by a Large Language Model, connected through LangChain's modern LCEL pipeline, and orchestrated through a shared memory system that makes them work as one unified brain.

This is not a chatbot. This is not a simple Q&A tool. This is a production-level agentic AI system the kind of architecture that top AI companies are actively building and hiring for right now.

Research Mind is an autonomous research pipeline that replicates the workflow of a human research team. Instead of relying on a single LLM's static training data, this system deploys **four specialized agents** that collaborate in real-time to produce high-fidelity, fact-checked reports on any complex topic.

It leverages the **LangChain Expression Language (LCEL)** for precise orchestration and the **Tavily Search API** for high-signal internet retrieval.


---

## 🔗 Live Demo
[https://research-mind-agents.streamlit.app/](https://research-mind-agents.streamlit.app/)

---

## 🏗️ How it Works
The project follows a linear, state-managed pipeline where data flows from one specialized agent to the next, refining information at every step.

### The Collaborative Workflow
```mermaid
graph TD
    User([User Topic Input]) --> Search{{🔎 Search Agent}}
    Search -- "Live Web Results" --> Reader{{📖 Reader Agent}}
    Reader -- "Extracted Knowledge" --> Writer{{✍️ Writer Agent}}
    Writer -- "Draft Report" --> Critic{{🧪 Critic Agent}}
    Critic -- "Score & Feedback" --> Output[🏁 Final Research Product]

    style Search fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style Reader fill:#bbf,stroke:#333,stroke-width:2px,color:#000
    style Writer fill:#bfb,stroke:#333,stroke-width:2px,color:#000
    style Critic fill:#fbb,stroke:#333,stroke-width:2px,color:#000
```

---

## ⚙️ Technical Implementation Details

### Phase 1: 🔎 The Search Agent (Information Retrieval)
The Search Agent is responsible for breaking out of the LLM's knowledge cutoff. It uses the **Tavily API** to find the most recent and reliable sources on the internet.
```mermaid
graph LR
    A[Topic Query] --> B[Search Agent]
    B --> C[Tavily API]
    C --> D[Ranked List of URLs & Snippets]
```

### Phase 2: 📖 The Reader Agent (Deep Context Extraction)
Unlike simple searchers, the Reader Agent actually "visits" the URLs. It uses **BeautifulSoup4** to scrape and clean the HTML, extracting only the meaningful text while discarding ads and navigation clutter.
```mermaid
graph LR
    A[Source URLs] --> B[Reader Agent]
    B --> C[BS4 Scraper]
    C --> D[Clean Research Context]
```

### Phase 3: ✍️ The Writer Agent (Synthesis & Generation)
The Writer Agent takes the raw intelligence and synthesizes it into a professional document. It uses **LangChain's LCEL** to ensure the output strictly follows a structured format (Intro, Key Findings, Conclusion).
```mermaid
graph LR
    A[Clean Context] --> B[Writer Chain]
    B --> C[GPT-4o-mini]
    C --> D[Structured Markdown Report]
```

### Phase 4: 🧪 The Critic Agent (Quality Assurance)
To ensure academic-grade quality, the Critic Agent reviews the draft. It scores the report out of 10 and provides specific "Areas to Improve," acting as a senior supervisor in the research loop.
```mermaid
graph LR
    A[Draft Report] --> B[Critic Agent]
    B --> C[Evaluation Logic]
    C --> D[Score + Feedback Report]
```

---

## ✨ Key Features
- **Autonomous Multi-Agent Orchestration**: Four agents working in sync with shared memory.
- **Real-time Web Scrutiny**: Bypasses knowledge cutoffs with live web searching and scraping.
- **LCEL Architecture**: Built using the modern LangChain Expression Language for modularity.
- **Interactive UI**: A polished Streamlit dashboard with live agent telemetry and progress tracking.
- **Feedback Loop**: Integrated critique phase to ensure high-quality output.

---

## 📂 Project Structure
```bash
Research_Mind_Agents/
├── agents.py           # Logic for Search, Reader, Writer, and Critic agents
├── pipeline.py         # The supervisor orchestrating the agent workflow
├── tools.py            # Custom Search (Tavily) and Scrape (BS4) tools
├── app.py              # Polished Streamlit UI with live status tracking
├── requirements.txt    # Project dependencies
└── .env                # API keys (OpenAI, Tavily)
```

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd Research_Mind_Agents
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file and add your keys:
```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Launch the App
```bash
streamlit run app.py
```

---
*Created with ❤️ by Gunjan Hirani*
