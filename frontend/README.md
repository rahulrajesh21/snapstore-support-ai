# SnapStore Support AI - Frontend

A modern, responsive customer support chat interface for SnapStore built to interface with the FastAPI RAG backend (`/api/v1/chat`).

## Features
- **Modern E-Commerce Theme:** Styled with Tailwind CSS, custom animations, and brand gradients.
- **Markdown & Code Rendering:** Safely renders structured text, bold points, bulleted lists, and tables via Marked.js and DOMPurify.
- **Suggested Inquiries:** One-click chips for common questions (Electronics returns, general policy, non-returnable items, human escalation).
- **Interactive Controls:**
  - Auto-resizing multi-line text input
  - Send on `Enter`, new line on `Shift + Enter`
  - Typing indicator while waiting for Pinecone + Gemini response
  - Copy-to-clipboard for assistant responses
  - Clear chat / Reset conversation
  - Friendly connection error handling with retry instructions

## How to Run

### Step 1: Start the Backend (Port 8000)
Make sure your virtual environment is active:
```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Step 2: Open the Frontend

#### Option A: VS Code Live Server (Port 5500)
Right-click `frontend/index.html` in VS Code and select **"Open with Live Server"**.

#### Option B: Python HTTP Server (Port 5500)
In a separate terminal tab:
```bash
python -m http.server 5500 --directory frontend
```
Then visit: [http://localhost:5500](http://localhost:5500)

#### Option C: Directly in Browser
You can also directly double-click or drag-and-drop `frontend/index.html` into Chrome, Safari, or Edge.
