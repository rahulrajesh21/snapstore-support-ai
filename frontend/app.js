// frontend/app.js

const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" 
  ? "http://127.0.0.1:8000" 
  : window.location.origin;

const API_ENDPOINT = `${API_BASE_URL}/api/v1/chat`;

// DOM Elements
const chatWindow = document.getElementById("chatWindow");
const messagesList = document.getElementById("messagesList");
const welcomeCard = document.getElementById("welcomeCard");
const typingIndicator = document.getElementById("typingIndicator");
const errorBanner = document.getElementById("errorBanner");
const errorMessage = document.getElementById("errorMessage");
const dismissError = document.getElementById("dismissError");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const suggestBtns = document.querySelectorAll(".suggest-btn");

let isWaitingForResponse = false;

// Configure Marked.js options
if (window.marked) {
  marked.setOptions({
    breaks: true,
    gfm: true
  });
}

// Auto-adjust textarea height
function autoResizeInput() {
  chatInput.style.height = "auto";
  chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + "px";
  
  // Enable / disable send button
  const hasText = chatInput.value.trim().length > 0;
  sendBtn.disabled = !hasText || isWaitingForResponse;
}

chatInput.addEventListener("input", autoResizeInput);

// Handle Enter and Shift+Enter
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) {
      chatForm.dispatchEvent(new Event("submit"));
    }
  }
});

// Dismiss Error Banner
dismissError.addEventListener("click", () => {
  errorBanner.classList.add("hidden");
});

function showError(msg) {
  errorMessage.textContent = msg;
  errorBanner.classList.remove("hidden");
}

function hideError() {
  errorBanner.classList.add("hidden");
}

// Scroll to bottom smoothly
function scrollToBottom() {
  setTimeout(() => {
    chatWindow.scrollTo({
      top: chatWindow.scrollHeight,
      behavior: "smooth"
    });
  }, 50);
}

// Format current time (HH:MM AM/PM)
function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// Append User Message to UI
function appendUserMessage(text) {
  welcomeCard.classList.add("hidden");

  const messageWrapper = document.createElement("div");
  messageWrapper.className = "flex justify-end items-end space-x-2.5 message-anim";

  const messageBubble = document.createElement("div");
  messageBubble.className = "max-w-[85%] sm:max-w-[75%] bg-brand-600 text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-sm";

  const textNode = document.createElement("p");
  textNode.className = "text-sm whitespace-pre-wrap leading-relaxed";
  textNode.textContent = text;

  const timeStamp = document.createElement("span");
  timeStamp.className = "block text-[10px] text-brand-200 mt-1 text-right";
  timeStamp.textContent = getCurrentTime();

  messageBubble.appendChild(textNode);
  messageBubble.appendChild(timeStamp);

  const avatar = document.createElement("div");
  avatar.className = "w-7 h-7 rounded-full bg-slate-300 text-slate-700 flex items-center justify-center text-xs flex-shrink-0 mb-1";
  avatar.innerHTML = `<i class="fa-solid fa-user"></i>`;

  messageWrapper.appendChild(messageBubble);
  messageWrapper.appendChild(avatar);

  messagesList.appendChild(messageWrapper);
  scrollToBottom();
}

// Append Assistant Message to UI
function appendAssistantMessage(rawContent) {
  const messageWrapper = document.createElement("div");
  messageWrapper.className = "flex items-start space-x-3 message-anim";

  const avatar = document.createElement("div");
  avatar.className = "w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-700 to-indigo-600 text-white flex items-center justify-center text-xs flex-shrink-0 shadow-sm mt-0.5";
  avatar.innerHTML = `<i class="fa-solid fa-headset"></i>`;

  const messageBubble = document.createElement("div");
  messageBubble.className = "max-w-[90%] sm:max-w-[80%] bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-4 py-3.5 shadow-sm text-slate-800 relative group";

  // Parse Markdown safely
  const parsedHtml = window.marked && window.DOMPurify 
    ? DOMPurify.sanitize(marked.parse(rawContent)) 
    : rawContent;

  const contentDiv = document.createElement("div");
  contentDiv.className = "prose-chat";
  contentDiv.innerHTML = parsedHtml;

  // Metadata Footer (Timestamp + Copy Button)
  const metaFooter = document.createElement("div");
  metaFooter.className = "flex items-center justify-between border-t border-slate-100 pt-2 mt-2.5 text-[11px] text-slate-400";

  const timeStamp = document.createElement("span");
  timeStamp.textContent = `${getCurrentTime()} • SnapStore Policy AI`;

  const copyBtn = document.createElement("button");
  copyBtn.className = "hover:text-brand-600 transition flex items-center space-x-1";
  copyBtn.innerHTML = `<i class="fa-regular fa-copy"></i><span>Copy</span>`;
  copyBtn.title = "Copy answer";

  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(rawContent).then(() => {
      copyBtn.innerHTML = `<i class="fa-solid fa-check text-emerald-500"></i><span class="text-emerald-600 font-medium">Copied!</span>`;
      setTimeout(() => {
        copyBtn.innerHTML = `<i class="fa-regular fa-copy"></i><span>Copy</span>`;
      }, 2000);
    });
  });

  metaFooter.appendChild(timeStamp);
  metaFooter.appendChild(copyBtn);

  messageBubble.appendChild(contentDiv);
  messageBubble.appendChild(metaFooter);

  messageWrapper.appendChild(avatar);
  messageWrapper.appendChild(messageBubble);

  messagesList.appendChild(messageWrapper);
  scrollToBottom();
}

// Send Message Handler
async function handleSendMessage(query) {
  if (!query || isWaitingForResponse) return;

  hideError();
  isWaitingForResponse = true;
  chatInput.value = "";
  autoResizeInput();

  appendUserMessage(query);

  // Show Typing Indicator
  typingIndicator.classList.remove("hidden");
  scrollToBottom();

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: query })
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    typingIndicator.classList.add("hidden");

    let reply = "";
    if (typeof data.response === "string") {
      reply = data.response;
    } else if (Array.isArray(data.response) && data.response[0]?.text) {
      reply = data.response.map(part => part.text || "").join("");
    } else {
      reply = JSON.stringify(data.response, null, 2);
    }

    appendAssistantMessage(reply);

  } catch (err) {
    typingIndicator.classList.add("hidden");
    console.error("Chat API Error:", err);

    showError(`Error connecting to backend (${API_ENDPOINT}). Ensure FastAPI is running with: uvicorn main:app --reload`);

    appendAssistantMessage(
      `⚠️ **Connection Error:** I was unable to reach the SnapStore Support API. \n\nPlease verify that your FastAPI backend is running on \`http://127.0.0.1:8000\`:\n\`\`\`bash\nuvicorn main:app --reload\n\`\`\``
    );
  } finally {
    isWaitingForResponse = false;
    autoResizeInput();
    chatInput.focus();
  }
}

// Form Submit Event
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const query = chatInput.value.trim();
  if (query) {
    handleSendMessage(query);
  }
});

// Suggested Prompt Chips
suggestBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const promptText = btn.querySelector("span:last-child").textContent;
    handleSendMessage(promptText);
  });
});

// Clear Chat Event
clearBtn.addEventListener("click", () => {
  messagesList.innerHTML = "";
  welcomeCard.classList.remove("hidden");
  hideError();
  chatInput.value = "";
  autoResizeInput();
  chatInput.focus();
});

// Initial focus
chatInput.focus();
