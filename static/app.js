const chat = document.getElementById("chat");
const input = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const statusEl = document.getElementById("status");
const speakToggle = document.getElementById("speakToggle");

function addBubble(text, who) {
  const div = document.createElement("div");
  div.className = `bubble ${who}`;
  div.textContent = text; // textContent prevents HTML injection
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
  if (!speakToggle.checked || !("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-IN";
  utterance.rate = 1;
  window.speechSynthesis.speak(utterance);
}

async function sendMessage(textFromVoice = null) {
  const message = (textFromVoice ?? input.value).trim();
  if (!message) return;
  addBubble(message, "user");
  input.value = "";
  statusEl.textContent = "Thinking...";
  sendBtn.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message})
    });
    const data = await response.json();
    const reply = data.reply || "I didn't receive a response.";
    addBubble(reply, "assistant");
    speak(reply);
    statusEl.textContent = data.action === "system" ? "System action" : "Ready";
  } catch (error) {
    addBubble("Connection error. Check that the Flask server is running.", "assistant");
    statusEl.textContent = "Offline";
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", () => sendMessage());
input.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

// Browser speech recognition with Hey Supreme wake word

const SpeechRecognition =window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let wakeWordEnabled = false;
let awaitingCommand = false;
let restartTimer = null;

if (SpeechRecognition) {
recognition = new SpeechRecognition();

recognition.lang = "en-IN";
recognition.continuous = false;
recognition.interimResults = false;

function startListening() {
if (!wakeWordEnabled) return;
try {
  recognition.start();
} catch (error) {
  console.log("Recognition start error:", error);
}
}

recognition.onstart = () => {
micBtn.textContent = "🟢 Hey Supreme Active";
statusEl.textContent = awaitingCommand
? "Waiting for your command..."
: "Say Hey Supreme";
};

recognition.onresult = event => {
const transcript =
event.results[event.results.length - 1][0].transcript.trim();

const text = transcript.toLowerCase();

if (!awaitingCommand) {
  if (text.includes("hey supreme")) {
    const command = text.replace("hey supreme", "").trim();

    if (command) {
      sendMessage(command);
    } else {
      awaitingCommand = true;
      recognition.stop();
      speak("Yes, I'm listening. What can I do for you?");
    }
  }
} else {
  awaitingCommand = false;
  sendMessage(transcript);
}

};

recognition.onerror = event => {
statusEl.textContent = `Mic error: ${event.error}`;
console.error("Speech recognition error:", event.error);
};

recognition.onend = () => {
if (wakeWordEnabled) {
clearTimeout(restartTimer);
restartTimer = setTimeout(startListening, 1000);
} else {
micBtn.textContent = "🎙 Enable Hey Supreme";
statusEl.textContent = "Wake word disabled";
}
};

micBtn.textContent = "🎙 Enable Hey Supreme";

micBtn.addEventListener("click", () => {
if (!wakeWordEnabled) {
wakeWordEnabled = true;
awaitingCommand = false;
startListening();
} else {
wakeWordEnabled = false;
awaitingCommand = false;
clearTimeout(restartTimer);
recognition.stop();

  micBtn.textContent = "🎙 Enable Hey Supreme";
  statusEl.textContent = "Wake word disabled";
}

});

} else {
micBtn.disabled = true;
micBtn.textContent = "Voice unavailable";
statusEl.textContent = "Use Chrome or Edge";
}
