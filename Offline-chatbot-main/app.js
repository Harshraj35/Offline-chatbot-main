document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const chatWindow = document.getElementById('chat-window');
    const messageForm = document.getElementById('message-form');
    const userInput = document.getElementById('user-input');
    const welcomeScreen = document.querySelector('.welcome-screen');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    const inputArea = document.getElementById('input-area');
    
    // Navigation Elements
    const btnChat = document.getElementById('btn-chat');
    const btnHistory = document.getElementById('btn-history');
    const btnSettings = document.getElementById('btn-settings');
    const views = {
        chat: chatWindow,
        history: document.getElementById('history-view'),
        settings: document.getElementById('settings-view')
    };
    const navItems = [btnChat, btnHistory, btnSettings];

    // Settings Elements
    const languageSelect = document.getElementById('language-select');
    const speedSlider = document.getElementById('speed-slider');
    const clearHistoryBtn = document.getElementById('clear-history');

    // State
    let currentLanguage = localStorage.getItem('language') || 'en';
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    let responseSpeed = parseInt(localStorage.getItem('responseSpeed')) || 1500;

    // Translations
    const translations = {
        en: {
            welcome: "How can I help you today?",
            description: "I'm your on-device AI assistant, capable of coding, reasoning, and task management.",
            placeholder: "Type your message here...",
            chat: "Chat",
            history: "History",
            settings: "Settings",
            onDevice: "On-Device Ready",
            clearAll: "Clear All",
            noHistory: "No past conversations found.",
            langLabel: "Language",
            speedLabel: "AI Response Speed",
            notifyLabel: "Notifications",
            typing: "...",
            aiHeader: "AI Assistant",
            aiSubheader: "Always active, totally private",
            suggestCode: "Write some code",
            suggestConcept: "Explain a concept",
            suggestHomework: "Help with homework"
        },
        hi: {
            welcome: "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?",
            description: "मैं आपका डिवाइस पर चलने वाला AI सहायक हूँ, जो कोडिंग और तर्क में सक्षम है।",
            placeholder: "अपना संदेश यहाँ लिखें...",
            chat: "चैट",
            history: "इतिहास",
            settings: "सेटिंग्स",
            onDevice: "डिवाइस पर तैयार",
            clearAll: "सब साफ़ करें",
            noHistory: "कोई पिछला इतिहास नहीं मिला।",
            langLabel: "भाषा",
            speedLabel: "AI प्रतिक्रिया गति",
            notifyLabel: "सूचनाएं",
            typing: "टाइप कर रहा है...",
            aiHeader: "AI सहायक",
            aiSubheader: "हमेशा सक्रिय, पूरी तरह निजी",
            suggestCode: "कोड लिखें",
            suggestConcept: "अवधारणा समझाएं",
            suggestHomework: "होमवर्क में मदद"
        }
    };

    // Initial Setup
    applyLanguage(currentLanguage);
    loadHistory();
    languageSelect.value = currentLanguage;
    speedSlider.value = responseSpeed;

    // View Switching Logic
    function switchView(viewName) {
        Object.keys(views).forEach(name => {
            if (name === viewName) {
                views[name].classList.add('active-view');
            } else {
                views[name].classList.remove('active-view');
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
        });

        if (viewName === 'chat') {
            btnChat.classList.add('active');
            inputArea.style.display = 'block';
        } else if (viewName === 'history') {
            btnHistory.classList.add('active');
            inputArea.style.display = 'none';
            renderHistory();
        } else if (viewName === 'settings') {
            btnSettings.classList.add('active');
            inputArea.style.display = 'none';
        }
    }

    btnChat.addEventListener('click', () => switchView('chat'));
    btnHistory.addEventListener('click', () => switchView('history'));
    btnSettings.addEventListener('click', () => switchView('settings'));

    // Language Logic
    languageSelect.addEventListener('change', (e) => {
        currentLanguage = e.target.value;
        localStorage.setItem('language', currentLanguage);
        applyLanguage(currentLanguage);
    });

    function applyLanguage(lang) {
        const t = translations[lang];
        document.querySelector('.welcome-screen h3').textContent = t.welcome;
        document.querySelector('.welcome-screen p').textContent = t.description;
        userInput.placeholder = t.placeholder;
        
        btnChat.querySelector('span:last-child').textContent = t.chat;
        btnHistory.querySelector('span:last-child').textContent = t.history;
        btnSettings.querySelector('span:last-child').textContent = t.settings;
        
        document.querySelector('.status-card span').textContent = t.onDevice;
        document.querySelector('.header-info h2').textContent = t.aiHeader;
        document.querySelector('.header-info p').textContent = t.aiSubheader;
        
        document.querySelector('#history-view h3').textContent = t.history;
        document.querySelector('#settings-view h3').textContent = t.settings;
        clearHistoryBtn.textContent = t.clearAll;
        
        const labels = document.querySelectorAll('.setting-group label');
        labels[0].textContent = t.langLabel;
        labels[1].textContent = t.speedLabel;
        labels[2].textContent = t.notifyLabel;

        document.getElementById('suggest-code').textContent = t.suggestCode;
        document.getElementById('suggest-concept').textContent = t.suggestConcept;
        document.getElementById('suggest-homework').textContent = t.suggestHomework;
    }

    // Response Speed logic
    speedSlider.addEventListener('input', (e) => {
        responseSpeed = parseInt(e.target.value);
        localStorage.setItem('responseSpeed', responseSpeed);
    });

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    });

    // Handle form submission
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            saveToHistory(message, 'user');
            userInput.value = '';
            userInput.style.height = 'auto';
            
            const currentWelcome = document.querySelector('.welcome-screen');
            if (currentWelcome) {
                currentWelcome.style.display = 'none';
            }

            simulateAIResponse(message);
        }
    });

    // Handle suggestion chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            userInput.value = chip.textContent;
            messageForm.dispatchEvent(new Event('submit'));
        });
    });

    function addMessage(text, sender, imageUrl = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        
        if (imageUrl) {
            const img = document.createElement('img');
            img.src = imageUrl;
            img.alt = 'Uploaded Image';
            img.style.maxWidth = '100%';
            img.style.borderRadius = '8px';
            img.style.marginTop = '8px';
            messageDiv.appendChild(img);
        }
        
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function saveToHistory(text, sender, imageUrl = null) {
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        chatHistory.push({ text, sender, timestamp, imageUrl });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }

    function loadHistory() {
        if (chatHistory.length > 0 && welcomeScreen) {
            welcomeScreen.style.display = 'none';
            chatHistory.forEach(msg => {
                addMessage(msg.text, msg.sender, msg.imageUrl);
            });
        }
    }

    function renderHistory() {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';
        
        if (chatHistory.length === 0) {
            historyList.innerHTML = `<div class="empty-state">${translations[currentLanguage].noHistory}</div>`;
            return;
        }

        // Show simplified history (only user messages as titles)
        const userMessages = chatHistory.filter(m => m.sender === 'user');
        if (userMessages.length === 0) {
            historyList.innerHTML = `<div class="empty-state">${translations[currentLanguage].noHistory}</div>`;
            return;
        }

        userMessages.reverse().forEach((msg, index) => {
            const item = document.createElement('div');
            item.classList.add('setting-group');
            item.style.cursor = 'pointer';
            item.innerHTML = `
                <div>
                    <div style="font-weight: 600;">${msg.text.substring(0, 30)}${msg.text.length > 30 ? '...' : ''}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">${msg.timestamp}</div>
                </div>
                <span>➡️</span>
            `;
            item.addEventListener('click', () => switchView('chat'));
            historyList.appendChild(item);
        });
    }

    clearHistoryBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all history?')) {
            clearEverything();
        }
    });

    document.getElementById('header-clear').addEventListener('click', () => {
        if (confirm('Clear current chat?')) {
            clearEverything();
        }
    });

    function clearEverything() {
        chatHistory = [];
        localStorage.removeItem('chatHistory');
        chatWindow.innerHTML = '';
        // Restore welcome screen
        const ws = document.createElement('div');
        ws.className = 'welcome-screen';
        ws.innerHTML = `
            <div class="welcome-icon">✨</div>
            <h3>${translations[currentLanguage].welcome}</h3>
            <p>${translations[currentLanguage].description}</p>
        `;
        chatWindow.appendChild(ws);
        renderHistory();
    }

    document.getElementById('header-export').addEventListener('click', () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(chatHistory));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "chat_history.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    });

    // Configuration
    const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:10000'
        : 'https://echomind-backend-w74f.onrender.com';

    async function simulateAIResponse(userText) {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'ai', 'typing');
        typingDiv.textContent = translations[currentLanguage].typing;
        chatWindow.appendChild(typingDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch(`${API_BASE_URL}/chat/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: userText,
                    language: currentLanguage
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            if (chatWindow.contains(typingDiv)) {
                chatWindow.removeChild(typingDiv);
            }

            const aiResponse = data.response;
            addMessage(aiResponse, 'ai');
            saveToHistory(aiResponse, 'ai');

        } catch (error) {
            console.error('Error:', error);
            if (chatWindow.contains(typingDiv)) {
                chatWindow.removeChild(typingDiv);
            }
            const errorMsg = currentLanguage === 'en' 
                ? "Error: Could not connect to the AI backend. Make sure the server is running."
                : "त्रुटि: ऑफ़लाइन AI बैकएंड से कनेक्ट नहीं हो सका। सुनिश्चित करें कि सर्वर चल रहा है।";
            addMessage(errorMsg, 'ai');
            saveToHistory(errorMsg, 'ai');
        }
    }

    // Enter to submit (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            messageForm.dispatchEvent(new Event('submit'));
        }
    });

    // File Upload functionality (Edge Gallery)
    const uploadImgBtn = document.getElementById('upload-img');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    // Allow images, PDFs, and text files for Edge Gallery
    fileInput.accept = 'image/*,.pdf,.txt';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    uploadImgBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            // If it's an image, show preview in chat
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const imgData = event.target.result;
                    addMessage(`Uploading file: ${file.name}`, 'user', imgData);
                    saveToHistory(`Uploading file: ${file.name}`, 'user', imgData);
                };
                reader.readAsDataURL(file);
            } else {
                addMessage(`Uploading file: ${file.name}`, 'user');
                saveToHistory(`Uploading file: ${file.name}`, 'user');
            }

            const currentWelcome = document.querySelector('.welcome-screen');
            if (currentWelcome) {
                currentWelcome.style.display = 'none';
            }

            const typingDiv = document.createElement('div');
            typingDiv.classList.add('message', 'ai', 'typing');
            typingDiv.textContent = translations[currentLanguage].typing;
            chatWindow.appendChild(typingDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;

            try {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('tags', 'chat_upload');

                const response = await fetch(`${API_BASE_URL}/gallery/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Upload failed');
                }

                if (chatWindow.contains(typingDiv)) {
                    chatWindow.removeChild(typingDiv);
                }

                const aiResponse = currentLanguage === 'en' 
                    ? `I have successfully saved ${file.name} to the Edge Gallery! You can now search or ask questions about it.`
                    : `मैंने एज गैलरी में ${file.name} सफलतापूर्वक सहेज लिया है! अब आप इसके बारे में खोज या प्रश्न पूछ सकते हैं।`;
                addMessage(aiResponse, 'ai');
                saveToHistory(aiResponse, 'ai');

            } catch (error) {
                console.error('Upload Error:', error);
                if (chatWindow.contains(typingDiv)) {
                    chatWindow.removeChild(typingDiv);
                }
                const errorMsg = currentLanguage === 'en' 
                    ? "Error: Could not upload to Edge Gallery. Is the backend server running?"
                    : "त्रुटि: एज गैलरी में अपलोड नहीं किया जा सका। क्या बैकएंड सर्वर चल रहा है?";
                addMessage(errorMsg, 'ai');
                saveToHistory(errorMsg, 'ai');
            }
        }
        fileInput.value = ''; // Reset input
    });

    // Voice Input functionality
    const voiceBtn = document.getElementById('voice-btn');
    let isRecording = false;

    voiceBtn.addEventListener('click', () => {
        if (!isRecording) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.lang = currentLanguage === 'en' ? 'en-US' : 'hi-IN';
                recognition.start();
                isRecording = true;
                voiceBtn.style.color = '#00ffcc'; // Highlight color for recording
                showToast(currentLanguage === 'en' ? "Listening..." : "सुन रहा हूँ...");

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    userInput.value += (userInput.value ? ' ' : '') + transcript;
                    userInput.style.height = 'auto';
                    userInput.style.height = (userInput.scrollHeight) + 'px';
                    isRecording = false;
                    voiceBtn.style.color = '';
                };

                recognition.onerror = (event) => {
                    console.error('Speech recognition error', event.error);
                    isRecording = false;
                    voiceBtn.style.color = '';
                    showToast(currentLanguage === 'en' ? "Microphone error." : "माइक्रोफ़ोन त्रुटि।");
                };

                recognition.onend = () => {
                    isRecording = false;
                    voiceBtn.style.color = '';
                };
            } else {
                showToast(currentLanguage === 'en' ? "Speech recognition not supported in this browser." : "इस ब्राउज़र में ध्वनि पहचान समर्थित नहीं है।");
            }
        }
    });

    function showToast(message) {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.backgroundColor = 'var(--bg-accent)';
        toast.style.color = 'var(--text-primary)';
        toast.style.padding = '10px 20px';
        toast.style.borderRadius = '8px';
        toast.style.marginTop = '10px';
        toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        toast.style.transition = 'opacity 0.3s ease';
        toastContainer.appendChild(toast);
        
        toastContainer.style.position = 'fixed';
        toastContainer.style.bottom = '80px';
        toastContainer.style.left = '50%';
        toastContainer.style.transform = 'translateX(-50%)';
        toastContainer.style.zIndex = '1000';
        toastContainer.style.display = 'flex';
        toastContainer.style.flexDirection = 'column';
        toastContainer.style.alignItems = 'center';

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
});
