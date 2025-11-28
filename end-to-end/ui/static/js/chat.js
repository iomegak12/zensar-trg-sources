// Chat interface functionality with local storage and real-time features
class ChatInterface {
    constructor() {
        this.API_BASE = '';  // Using same domain as UI
        this.currentChatId = null;
        this.conversations = this.loadConversations();
        this.isTyping = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.initializeElements();
        this.bindEvents();
        this.loadChatHistory();
        this.updateConnectionStatus('connected');
        
        console.log('Chat interface initialized');
    }

    initializeElements() {
        this.elements = {
            chatMessages: document.getElementById('chatMessages'),
            messageInput: document.getElementById('messageInput'),
            sendBtn: document.getElementById('sendBtn'),
            chatHistory: document.getElementById('chatHistory'),
            newChatBtn: document.getElementById('newChatBtn'),
            clearHistoryBtn: document.getElementById('clearHistoryBtn'),
            connectionStatus: document.getElementById('connectionStatus'),
            charCount: document.getElementById('charCount'),
            loadingModal: new bootstrap.Modal(document.getElementById('loadingModal')),
            errorModal: new bootstrap.Modal(document.getElementById('errorModal'))
        };
    }

    bindEvents() {
        // Send message events
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Character count
        this.elements.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeInput();
        });

        // Chat management
        this.elements.newChatBtn.addEventListener('click', () => this.startNewChat());
        this.elements.clearHistoryBtn.addEventListener('click', () => this.clearAllHistory());

        // Auto-save on page unload
        window.addEventListener('beforeunload', () => this.saveConversations());
        
        // Focus message input on load
        this.elements.messageInput.focus();
    }

    updateCharCount() {
        const current = this.elements.messageInput.value.length;
        const max = 1000;
        this.elements.charCount.textContent = current;
        
        // Update styling based on length
        if (current > max * 0.9) {
            this.elements.charCount.className = 'text-warning';
        } else if (current === max) {
            this.elements.charCount.className = 'text-danger';
        } else {
            this.elements.charCount.className = 'text-muted';
        }
        
        // Disable send button if over limit
        this.elements.sendBtn.disabled = current === 0 || current > max || this.isTyping;
    }

    autoResizeInput() {
        const input = this.elements.messageInput;
        input.style.height = 'auto';
        const newHeight = Math.min(input.scrollHeight, 120);
        input.style.height = newHeight + 'px';
    }

    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || this.isTyping) return;

        try {
            // Add user message to chat
            this.addMessage(message, 'user');
            this.elements.messageInput.value = '';
            this.updateCharCount();
            this.autoResizeInput();

            // Show loading state
            this.setTyping(true);
            this.showTypingIndicator();

            // Send to API
            const response = await this.callAPI(message);
            
            // Remove typing indicator and add response
            this.hideTypingIndicator();
            this.addMessage(response.answer, 'bot', response);
            
            // Save conversation
            this.saveCurrentConversation();

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.showError('Failed to send message. Please try again.');
        } finally {
            this.setTyping(false);
            this.scrollToBottom();
        }
    }

    async callAPI(message) {
        this.updateConnectionStatus('connecting');
        
        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    question: message,
                    user_id: this.getUserId(),
                    session_id: this.currentChatId || this.generateSessionId()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.updateConnectionStatus('connected');
            this.reconnectAttempts = 0;
            
            return data;

        } catch (error) {
            this.updateConnectionStatus('error');
            this.reconnectAttempts++;
            
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                console.log(`Retrying... Attempt ${this.reconnectAttempts}`);
                await this.delay(1000 * this.reconnectAttempts);
                return this.callAPI(message);
            }
            
            throw error;
        }
    }

    addMessage(content, sender, metadata = {}) {
        const messageGroup = document.createElement('div');
        messageGroup.className = `message-group ${sender}-message`;
        
        const timestamp = new Date().toISOString();
        const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        messageGroup.innerHTML = `
            <div class="message-avatar">
                <span class="avatar ${sender === 'user' ? 'bg-primary' : 'bg-success'}">
                    ${sender === 'user' ? 
                        `<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/></svg>` :
                        `<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M8 9h8"/><path d="M8 13h6"/><path d="M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12z"/></svg>`
                    }
                </span>
            </div>
            <div class="message-content">
                <div class="message-bubble" data-message-id="${messageId}">
                    <div class="message-header">
                        <strong>${sender === 'user' ? 'You' : 'Agentic RAG Assistant'}</strong>
                        <span class="message-time" data-time="${timestamp}">${this.formatTime(timestamp)}</span>
                    </div>
                    <div class="message-text">${this.formatMessage(content)}</div>
                    ${metadata.sources ? this.renderSources(metadata.sources) : ''}
                    ${metadata.reflection ? this.renderReflection(metadata.reflection) : ''}
                </div>
            </div>
        `;

        this.elements.chatMessages.appendChild(messageGroup);
        
        // Add to current conversation
        if (!this.currentChatId) {
            this.currentChatId = this.generateSessionId();
        }
        
        this.addToCurrentConversation({
            id: messageId,
            content,
            sender,
            timestamp,
            metadata
        });

        this.scrollToBottom();
    }

    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>')
            .replace(/https?:\/\/[^\s]+/g, '<a href="$&" target="_blank" rel="noopener">$&</a>');
    }

    renderSources(sources) {
        if (!sources || sources.length === 0) return '';
        
        return `
            <div class="message-sources mt-3">
                <div class="small text-muted mb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-sm me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M14 3v4a1 1 0 0 0 1 1h4"/><path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"/></svg>
                    Sources:
                </div>
                ${sources.map((source, index) => `
                    <div class="source-item small">
                        <span class="badge badge-outline me-2">${index + 1}</span>
                        <span class="text-truncate">${source}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderReflection(reflection) {
        if (!reflection) return '';
        
        return `
            <div class="message-reflection mt-3">
                <details class="small">
                    <summary class="text-muted cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-sm me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M9 12l2 2l4 -4"/><circle cx="12" cy="12" r="9"/></svg>
                        AI Reasoning Process
                    </summary>
                    <div class="mt-2 p-2 bg-light rounded">
                        ${this.formatMessage(reflection)}
                    </div>
                </details>
            </div>
        `;
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'message-group bot-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <span class="avatar bg-success">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M8 9h8"/><path d="M8 13h6"/><path d="M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12z"/></svg>
                </span>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <span class="typing-dots">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </span>
                        <span class="ms-2">AI is thinking...</span>
                    </div>
                </div>
            </div>
        `;
        
        this.elements.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    setTyping(isTyping) {
        this.isTyping = isTyping;
        this.elements.sendBtn.disabled = isTyping || this.elements.messageInput.value.trim().length === 0;
        this.elements.messageInput.disabled = isTyping;
        
        if (isTyping) {
            this.elements.sendBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status"></span>
                <span class="visually-hidden">Loading...</span>
            `;
        } else {
            this.elements.sendBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><line x1="10" y1="14" x2="21" y2="3"/><path d="M21 3l-6.5 18a.55 .55 0 0 1 -1 0l-3.5 -7l-7 -3.5a.55 .55 0 0 1 0 -1l18 -6.5"/></svg>
                Send
            `;
        }
    }

    updateConnectionStatus(status) {
        const statusEl = this.elements.connectionStatus;
        const statusDot = statusEl.querySelector('.status-dot');
        
        statusEl.className = 'status-indicator';
        statusDot.className = 'status-dot';
        
        switch (status) {
            case 'connected':
                statusDot.classList.add('status-dot-animated', 'bg-green');
                statusEl.innerHTML = statusEl.innerHTML.replace(/Connected|Connecting|Disconnected/, 'Connected');
                break;
            case 'connecting':
                statusDot.classList.add('status-dot-animated', 'bg-yellow');
                statusEl.innerHTML = statusEl.innerHTML.replace(/Connected|Connecting|Disconnected/, 'Connecting');
                break;
            case 'error':
                statusDot.classList.add('bg-red');
                statusEl.innerHTML = statusEl.innerHTML.replace(/Connected|Connecting|Disconnected/, 'Disconnected');
                break;
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        }, 100);
    }

    // Chat management functions
    startNewChat() {
        this.currentChatId = this.generateSessionId();
        this.clearChatMessages();
        this.addWelcomeMessage();
        this.elements.messageInput.focus();
        this.updateChatHistory();
    }

    clearChatMessages() {
        this.elements.chatMessages.innerHTML = '';
    }

    addWelcomeMessage() {
        this.addMessage(`Hello! I'm your AI assistant powered by Agentic RAG technology. I can help you with:
        
• Answering questions using multiple knowledge sources
• Research and analysis from Wikipedia, Google, and Arxiv
• Self-reflective reasoning and quality checks
• Document retrieval and synthesis

How can I assist you today?`, 'bot');
    }

    clearAllHistory() {
        if (confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
            this.conversations = {};
            this.saveConversations();
            this.updateChatHistory();
            this.startNewChat();
        }
    }

    // Local storage functions
    loadConversations() {
        try {
            const stored = localStorage.getItem('agenticrag_conversations');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.error('Error loading conversations:', error);
            return {};
        }
    }

    saveConversations() {
        try {
            localStorage.setItem('agenticrag_conversations', JSON.stringify(this.conversations));
        } catch (error) {
            console.error('Error saving conversations:', error);
        }
    }

    addToCurrentConversation(message) {
        if (!this.currentChatId) return;
        
        if (!this.conversations[this.currentChatId]) {
            this.conversations[this.currentChatId] = {
                id: this.currentChatId,
                title: this.generateChatTitle(message.content),
                messages: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
        }
        
        this.conversations[this.currentChatId].messages.push(message);
        this.conversations[this.currentChatId].updatedAt = new Date().toISOString();
        
        // Update title if it's the first user message
        if (message.sender === 'user' && this.conversations[this.currentChatId].messages.filter(m => m.sender === 'user').length === 1) {
            this.conversations[this.currentChatId].title = this.generateChatTitle(message.content);
        }
        
        this.updateChatHistory();
    }

    saveCurrentConversation() {
        this.saveConversations();
    }

    generateChatTitle(message) {
        const words = message.split(' ').slice(0, 6).join(' ');
        return words.length > 30 ? words.substring(0, 30) + '...' : words;
    }

    generateSessionId() {
        return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getUserId() {
        let userId = localStorage.getItem('agenticrag_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('agenticrag_user_id', userId);
        }
        return userId;
    }

    updateChatHistory() {
        const historyEl = this.elements.chatHistory;
        const conversations = Object.values(this.conversations).sort((a, b) => 
            new Date(b.updatedAt) - new Date(a.updatedAt)
        );

        if (conversations.length === 0) {
            historyEl.innerHTML = `
                <div class="list-group-item text-muted text-center py-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-lg mb-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M8 9h8"/><path d="M8 13h6"/><path d="M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12z"/></svg>
                    <div>No conversations yet</div>
                    <small class="text-muted">Start a new chat to begin</small>
                </div>
            `;
            return;
        }

        historyEl.innerHTML = conversations.map(conv => `
            <div class="chat-history-item ${conv.id === this.currentChatId ? 'active' : ''}" 
                 data-chat-id="${conv.id}">
                <div class="chat-history-title">${conv.title}</div>
                <div class="chat-history-preview">
                    ${conv.messages[conv.messages.length - 1]?.content.substring(0, 50) || ''}${conv.messages[conv.messages.length - 1]?.content.length > 50 ? '...' : ''}
                </div>
                <div class="chat-history-time">${this.formatTime(conv.updatedAt)}</div>
            </div>
        `).join('');

        // Add click handlers
        historyEl.querySelectorAll('.chat-history-item').forEach(item => {
            item.addEventListener('click', () => {
                const chatId = item.dataset.chatId;
                this.loadConversation(chatId);
            });
        });
    }

    loadChatHistory() {
        this.updateChatHistory();
        
        // Load the most recent conversation or start new chat
        const conversations = Object.values(this.conversations).sort((a, b) => 
            new Date(b.updatedAt) - new Date(a.updatedAt)
        );
        
        if (conversations.length > 0) {
            this.loadConversation(conversations[0].id);
        } else {
            this.addWelcomeMessage();
        }
    }

    loadConversation(chatId) {
        const conversation = this.conversations[chatId];
        if (!conversation) return;

        this.currentChatId = chatId;
        this.clearChatMessages();

        conversation.messages.forEach(message => {
            const messageGroup = document.createElement('div');
            messageGroup.className = `message-group ${message.sender}-message`;
            
            messageGroup.innerHTML = `
                <div class="message-avatar">
                    <span class="avatar ${message.sender === 'user' ? 'bg-primary' : 'bg-success'}">
                        ${message.sender === 'user' ? 
                            `<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"/></svg>` :
                            `<svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="m0 0h24v24H0z" fill="none"/><path d="M8 9h8"/><path d="M8 13h6"/><path d="M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12z"/></svg>`
                        }
                    </span>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="message-header">
                            <strong>${message.sender === 'user' ? 'You' : 'Agentic RAG Assistant'}</strong>
                            <span class="message-time">${this.formatTime(message.timestamp)}</span>
                        </div>
                        <div class="message-text">${this.formatMessage(message.content)}</div>
                        ${message.metadata?.sources ? this.renderSources(message.metadata.sources) : ''}
                        ${message.metadata?.reflection ? this.renderReflection(message.metadata.reflection) : ''}
                    </div>
                </div>
            `;
            
            this.elements.chatMessages.appendChild(messageGroup);
        });

        this.updateChatHistory();
        this.scrollToBottom();
    }

    // Utility functions
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffMinutes = Math.floor(diffTime / (1000 * 60));
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

        if (diffMinutes < 1) {
            return 'Just now';
        } else if (diffMinutes < 60) {
            return `${diffMinutes}m ago`;
        } else if (diffHours < 24) {
            return `${diffHours}h ago`;
        } else if (diffDays < 7) {
            return `${diffDays}d ago`;
        } else {
            return date.toLocaleDateString();
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showError(message) {
        const errorMessageEl = document.getElementById('errorMessage');
        errorMessageEl.textContent = message;
        this.elements.errorModal.show();
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.chatInterface = new ChatInterface();
    console.log('Chat interface ready');
});

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatInterface;
}