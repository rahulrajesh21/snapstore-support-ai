# SnapStore Support AI - Frontend

A modern, responsive customer support chat interface for SnapStore built to interface with the FastAPI RAG backend (`/api/v1/chat`).

## Features
- **Multi-Domain Coverage:** Handles 5 comprehensive policy areas:
  - **Returns and Refunds:** Master return windows, exceptions, non-returnable categories, restocking fees.
  - **Shipping and Delivery:** Standard/Expedited/Priority tiers, free shipping thresholds, carrier GPS dispute policies, international DDP/DDU terms.
  - **Hardware Warranty and Care+:** 12-month standard warranty, SnapStore Care+ deductibles ($29 screen, $99 accidental replacement), RMA authorization flow.
  - **Payments and Billing:** Accepted methods, BNPL (Klarna/Afterpay), non-expiring store gift cards, and 7-day price match guarantees.
  - **Account Security and Privacy:** 12+ character password complexity, 2FA authenticator app enforcement, suspicious activity lockouts, GDPR/CCPA data export/deletion.
- **Modern Theme:** Styled with Tailwind CSS, custom animations, domain badges, and brand gradients.
- **Multi-Turn Session Threads:** Automatically maintains and sends `session_id` to the LangGraph memory checkpointer, allowing contextual follow-ups per session.
- **New Chat and Session Reset:** Dedicated button resets the conversation window and generates a fresh thread identifier.
- **Markdown and Code Rendering:** Safely renders structured headings, bold text, bullet points, blockquotes, and tables via Marked.js and DOMPurify.
- **Suggested Inquiries:** One-click chips spanning each policy domain.
- **Interactive Controls:**
  - Auto-resizing multi-line text input
  - Send on Enter, new line on Shift + Enter
  - Typing indicator while waiting for hybrid BM25 + Pinecone retrieval and Gemini reasoning
  - Copy-to-clipboard for assistant responses
  - Connection error handling with retry instructions

## How to Run

### Step 1: Start the Backend (Port 8000)
Make sure your virtual environment is active:
```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Step 2: Open the Frontend

#### Option A: VS Code Live Server (Port 5500)
Right-click `frontend/index.html` in VS Code and select "Open with Live Server".

#### Option B: Python HTTP Server (Port 5500)
In a separate terminal tab:
```bash
python -m http.server 5500 --directory frontend
```
Then visit: [http://localhost:5500](http://localhost:5500)

#### Option C: Directly in Browser
You can also directly double-click or open `frontend/index.html` in Chrome, Safari, or Edge.
