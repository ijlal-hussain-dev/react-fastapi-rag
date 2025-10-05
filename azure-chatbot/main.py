import logging
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import sys
from endpoints import setup_endpoints, blob_endpoints, search_endpoints
from fastapi.middleware.cors import CORSMiddleware
from env.config import settings

# Load .env file at the top
load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Azure Chatbot API", version="1.0")

# --- CORS Configuration ---
# For production, replace with specific frontend domains (e.g., "https://yourfrontend.com").
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    "*" # Allows all origins for development simplicity
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Domains allowed to access the API
    allow_credentials=True,             # Allow cookies/auth headers
    allow_methods=["*"],                # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],                # Allow all headers
)


# Include routers from separate files
app.include_router(setup_endpoints.router)
#app.include_router(indexer_endpoints.router)
app.include_router(blob_endpoints.router)
app.include_router(search_endpoints.router)

if __name__ == "__main__":
    try:
        # --- DIAGNOSTIC STEP ---
        print(f"--- RUNNING SERVER PROGRAMMATICALLY ---")
        print(f"--- UVICORN_PORT read from settings: {settings.UVICORN_PORT} ---")
        
        # FIX: Passing the app as an import string ("__main__:app") allows 'reload=True' to work correctly.
        uvicorn.run(
            "__main__:app",
            # Use 0.0.0.0 to bind to all interfaces (common for docker/production)
            host="127.0.0.1", 
            # Using the dynamic setting
            port=settings.UVICORN_PORT, 
            reload=True
        )
        
    except Exception as e:
        print(f"--- FAILED TO START SERVER ---", file=sys.stderr)
        print(f"An error occurred, likely due to a configuration/import issue.", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        print(f"Please ensure 'env.config' is correct and all environment variables are set.", file=sys.stderr)
