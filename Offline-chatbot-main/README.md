# EchoMind AI Assistant 🚀

A premium, offline-capable, and responsive AI chatbot interface designed for both mobile and desktop. This project leverages modern web technologies to provide a high-performance, private, and aesthetically pleasing user experience.

![Chatbot Preview](https://img.shields.io/badge/UI-Glassmorphism-blue)
![PWA](https://img.shields.io/badge/PWA-Ready-green)
![Offline](https://img.shields.io/badge/Offline-Capable-blueviolet)

---

## ✨ Features

### 💎 Premium UI/UX
- **Glassmorphism Design**: Sleek, transparent backgrounds with backdrop-blur effects.
- **Midnight Theme**: A deep, dark mode optimized for focus and visual comfort.
- **Fluid Animations**: Smooth message transitions and view switching.
- **Dynamic Input**: Auto-expanding textarea for long messages.

### 🧠 Smart Functionality
- **Bilingual Support**: Fully localized in English and Hindi (हिन्दी), switchable on the fly.
- **Persistent History**: Chat sessions are saved locally using `localStorage` and persist across reloads.
- **Settings Panel**: Customize AI response speed and manage language preferences.
- **Data Export**: Easily export your entire chat history as a JSON file.

### 📱 Fully Responsive
- **Desktop Pro View**: Features a persistent sidebar for seamless navigation between Chat, History, and Settings.
- **Mobile Optimized**: A clean, full-screen chat interface that adapts beautifully to any screen size.

### 🌐 Offline Power (PWA)
- **Installable**: Add to Home Screen on mobile or install as a desktop app.
- **Service Worker**: Core assets are cached locally, allowing the UI to load instantly without internet.
- **Privacy First**: All interactions and history are processed and stored entirely on your device.

---

## 🛠️ Tech Stack
- **HTML5**: Semantic structure and interactive views.
- **CSS3**: Custom properties, Flexbox, Grid, and Backdrop-filter.
- **JavaScript (ES6+)**: Core logic, DOM manipulation, state management, and translations.
- **PWA**: Web App Manifest and Service Workers.

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (recommended for the dev server)

### Installation
1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd "Offline chatbot"
   ```

### Running the App
To fully experience the PWA and Offline features, it is recommended to run the app through a local server:

```bash
npm run dev
```
*Note: If you don't have npm installed, you can simply open `index.html` in your browser, though some Service Worker features may be restricted.*

---

## 📂 Project Structure
```text
├── index.html       # Main application entry point and UI views
├── index.css        # Premium styling, animations, and design system
├── app.js           # Interactive logic, translations, and state management
├── sw.js            # Service Worker for offline caching
├── manifest.json    # PWA configuration
└── package.json     # Node scripts and project metadata
```

---

## 🔮 Roadmap
- [ ] **AI Integration**: Connect to local LLMs (WebLLM) or OpenAI/Gemini APIs.
- [x] **History Persistence**: Use `localStorage` to save conversations.
- [ ] **Voice Commands**: Integrated STT (Speech-to-Text) using Web Speech API.
- [ ] **Theming**: Customizable color accents and expanded language support.

---

## 📝 License
This project is open-source and free to use.

---
*Created with ❤️ by EchoMind AI*
