### React-FastAPI RAG: Enterprise-Grade AI Chatbot

![Architecture](https://img.shields.io/badge/Architecture-RAG-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![Azure](https://img.shields.io/badge/Cloud-Azure-0078D4)

This repository provides a production-ready template for a Retrieval-Augmented Generation (RAG) application. It leverages a modern decoupled architecture to deliver high-performance, AI-driven insights from unstructured data.

* **Frontend:** React 18, TypeScript, Vite, and Bootstrap for a type-safe, responsive UI.
* **Backend:** FastAPI (Python 3.10+) serving as a high-concurrency gateway to Azure AI.
* **Storage & Search**: Azure Blob Storage for raw data ingestion and Azure AI Search for vector-indexed retrieval


##  Technical StackLayer

| Layer                 | Technologies |
| ----------------------|:-----------------------------------:|
| User Interface        | React, TypeScript, Vite, Axios      |
| API Framework         | FastAPI (Pydantic v2, Uvicorn)      |
| AI Orchestration      | Azure OpenAI / RAG Pattern          |
| Infrastructure        | Azure Search, Azure Blob Storage    |
| DevOps                | Dotenv, Virtual Environments, NPM   |


## Getting Started
Follow these steps to get your local development environment running.

**Prerequisites** 
You will need the following installed on your system:
* Python (3.8+)
* Node.js (18+ recommended)


#### 1. Backend Setup (FastAPI - Python)
The backend code is located in the root directory [azure-chatbot].
```
A. Environment Setup
Create and Activate a Virtual Environment:

python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

Install Python Dependencies:

pip install -r requirements.txt
# (Assuming you have a requirements.txt, if not, you need fastapi, uvicorn, python-dotenv, and pydantic)

B. Configuration (.env)
Create a file named .env in the root directory and populate it with your environment variables. At a minimum, you must define the port:
```
#### Backend Server Configuration
- UVICORN_PORT=9900 , default port is : 8000
- HOST_URL="[http://127.0.0.1](http://127.0.0.1)" # Used for local testing
- Azure AI Service Credentials (Example - adjust names based on your env/config.py)
- AZURE_SEARCH_SERVICE_NAME=your-search-service
- AZURE_SEARCH_API_KEY=your-search-key
- AZURE_BLOB_STORAGE_ACCOUNT_URL=[https://yourstorageaccount.blob.core.windows.net](https://yourstorageaccount.blob.core.windows.net)
- ... other configurations
#### Run the Backend
Ensure your virtual environment is active, and run the main file directly (this ensures your custom port from .env is used):

```
fastapi dev main.py (defult port) OR python main.py (customized port) 
```
The API will start, typically running on http://0.0.0.0:9900 (or the port specified in UVICORN_PORT).

#### 2. Frontend Setup (React/TypeScript/Vite)
The frontend code is assumed to be located in the frontend/ subdirectory.

A. Environment Setup
Navigate to the Frontend Directory [azure-chatbot-ui]:
```
cd frontend
Install Node Dependencies:
npm install
B. Configuration (.env)
Create a file named .env in the frontend/ directory to store environment variables accessible by Vite.

# Frontend Configuration
# This variable is crucial for the React app to know where the FastAPI backend is.
VITE_API_BASE_URL=http://localhost:9900

# Optionally set the frontend dev port (Vite defaults to 5173 or 3000)
VITE_DEV_PORT=3000

C. Run the Frontend
Run the development server:

npm run dev
```
The React application will start http://localhost:3005/, usually on http://localhost:3000 or http://localhost:5173.
