const { useState, useEffect, useRef } = React;

// Add this near the top of the file, after the React imports
const apiService = {
    async sendChatMessage(message, sessionId) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, session_id: sessionId })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response from API');
        }
        
        return response.json();
    },

    async refreshIndex() {
        return mockApiCall('/api/refresh-index');
    },

    async getHistory(sessionId) {
        const response = await fetch(`/api/get-history?session_id=${sessionId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch chat history');
        }
        return response.json();
    }
};

// Mock API with alternating success and error responses to simulate real-world API behavior
let callCount = 0;
const mockApiCall = (endpoint, data) => new Promise((resolve, reject) => {
    setTimeout(() => {
        callCount++;
        if (callCount % 2 === 0) {
            // Simulate an error response every other call
            reject(new Error("An error occurred while processing your request."));
        } else {
            resolve({ success: true, message: "Index refreshed successfully." });
        }
    }, 1000); // Simulated network latency of 1 second
});

/**
 * Notification Component
 * Displays temporary success or error messages to the user.
 * Automatically dismisses after 3 seconds.
 */
const Notification = ({ message, type, onClose }) => {
    useEffect(() => { 
        const timer = setTimeout(onClose, 2000); // Auto-close notification
        lucide.createIcons();
        return () => clearTimeout(timer); // Cleanup timer on unmount
    }, [onClose]);

    // Determine background color and icon based on notification type
    const bgColor = type === 'error' ? 'bg-red-500' : 'bg-green-500';
    const icon = type === 'error' ? 'alert-circle' : 'check-circle';

    return (
        <div className={`${bgColor} text-white text-sm px-4 py-2 rounded-lg shadow-lg fade-in flex items-center`}>
            <i data-lucide={icon} className="w-4 h-4 mr-2"></i>
            {message}
        </div>
    );
};

/**
 * Chat Component
 * Root component managing the chat interface, including message handling, API interactions,
 * and integrating other sub-components like Header, ChatWindow, Actions, and Footer.
 */
const Chat = () => {
    // State variables to manage messages, user input, loading states, and notifications
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [notification, setNotification] = useState(null);
    const [sessionId, setSessionId] = useState(() => localStorage.getItem('session_id') || generateUUID());

    // Save chatUuid to localStorage to persist across reloads
    useEffect(() => {
        localStorage.setItem('session_id', sessionId);
    }, [sessionId]);

    // Refs to manage scrolling and input focus
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    /**
     * Scrolls the chat window to the bottom
     */
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    /**
     * Effect Hook: Scrolls to the bottom of the chat window whenever messages or notifications change.
     * Also initializes Lucide icons after updates.
     */
    useEffect(() => { 
        const fetchHistory = async () => {
            try {
                const history = await apiService.getHistory(sessionId);
                const formattedHistory = history.map(([text, isUser]) => ({
                    text,
                    isUser: Boolean(isUser)
                }));
                setMessages(formattedHistory);
                scrollToBottom();
            } catch (error) {
                console.error('Error fetching chat history:', error);
            }
        };

        fetchHistory();
        lucide.createIcons(); // Initialize icons after DOM updates
    }, [sessionId]);

    /**
     * Effect Hook: Automatically focuses the input field when the component mounts.
     */
    useEffect(() => { 
        inputRef.current?.focus(); 
    }, []);

    /**
     * Sends a user message and handles the API response.
     * Updates the message list with user input and AI response or error.
     */
    const sendMessage = async (e) => {
        e.preventDefault();
        const trimmedInput = input.trim();
        if (!trimmedInput) return; // Prevent sending empty messages

        setIsLoading(true);
        // Add user's message to the chat
        const userMessage = { text: trimmedInput, isUser: true };
        setMessages(prev => [...prev, userMessage]);
        setInput(''); // Clear input field

        try {
            const data = await apiService.sendChatMessage(trimmedInput, sessionId);
            const aiMessage = { text: data.response, isUser: false };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            // Handle and display error message in chat
            const errorMessage = { text: error.message, isUser: false };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
            inputRef.current?.focus(); // Refocus input after sending
            scrollToBottom();
        }
    };

    /**
     * Refreshes the index by calling the respective API endpoint.
     * Displays a notification based on success or failure.
     */
    const refreshIndex = async () => {
        setIsRefreshing(true);
        try {
            const response = await apiService.refreshIndex();
            // Show success notification upon successful index refresh
            setNotification({ message: response.message, type: 'success' });
        } catch (error) {
            // Show error notification if refresh fails
            setNotification({ message: error.message, type: 'error' });
        } finally {
            setIsRefreshing(false);
        }
    };

    /**
     * Resets the chat by clearing all messages and input.
     * Generates a new session_id.
     * Provides user feedback via a notification.
     */
    const resetChat = async () => {
        try {
            setSessionId(generateUUID());
            setMessages([]);
            setInput('');
            setNotification({ message: "Chat history cleared", type: 'success' });
        } catch (error) {
            setNotification({ message: error.message, type: 'error' });
        }
    };

    return (
        <div className="md:w-[600px] w-full mx-auto bg-white rounded-xl shadow-2xl overflow-hidden">
            <Header />
            <ChatWindow 
                messages={messages} 
                isLoading={isLoading}
                sendMessage={sendMessage}
                input={input}
                setInput={setInput}
                inputRef={inputRef} 
                messagesEndRef={messagesEndRef}
            />
            <Actions 
                refreshIndex={refreshIndex} 
                resetChat={resetChat}
                isRefreshing={isRefreshing} 
                notification={notification} 
                setNotification={setNotification} 
            />
            <Footer />
        </div>
    );
};

/**
 * Header Component
 * Displays the application's header with title and attribution.
 */
const Header = () => (
    <header className="bg-gradient-to-r from-indigo-600 to-indigo-800 text-white p-6 py-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <h1 className="text-xl font-bold">Demo Finance RAG</h1>
            <div className="flex items-center text-sm space-x-2 mt-2 sm:mt-0 justify-end pl-8">
                <span>Powered by <a href="https://llamaindex.ai" target="_blank" rel="noopener noreferrer" className="underline">llama_index</a></span>
                <i data-lucide="database" className="w-4 h-4"></i>
            </div>
        </div>
    </header>
);

/**
 * ChatWindow Component
 * Renders the chat messages, input field, and send button.
 * Handles the display of loading indicators and message styling.
 */
const ChatWindow = ({ messages, isLoading, sendMessage, input, setInput, inputRef, messagesEndRef }) => (
    <div className="p-6 h-[calc(100vh-240px)] min-h-[300px] flex flex-col">
        <div className="bg-gray-50 rounded-lg border border-gray-200 shadow-inner overflow-hidden flex-1">
            <div className="h-full overflow-y-auto p-4 space-y-4" style={{ scrollBehavior: 'smooth' }}>
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-4">
                        Start a conversation by sending a message.
                    </div>
                )}
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow-md ${msg.isUser 
                            ? 'bg-gradient-to-r from-indigo-500 to-indigo-600 text-white ml-auto' 
                            : 'bg-white border border-gray-200'} fade-in`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg typing-indicator">
                            AI is thinking
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} /> {/* Reference point to scroll into view */}
            </div>
        </div>
        <form onSubmit={sendMessage} className="pt-6 bg-white rounded-b-lg">
            <div className="flex border border-gray-200 rounded-lg overflow-hidden transition-all duration-200">
                <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder="Ask a question..."
                    className="flex-grow px-4 py-2 focus:outline-none"
                    disabled={isLoading} // Disable input while loading
                />
                <button
                    type="submit"
                    className="bg-indigo-500 text-white px-6 py-2 hover:bg-indigo-600 disabled:opacity-50 transition-all duration-200 flex items-center"
                    disabled={isLoading} // Disable button while loading
                >
                    <span>{isLoading ? 'Sending...' : 'Send'}</span>
                    <i data-lucide={isLoading ? 'loader' : 'send'} className="w-4 h-4 ml-2"></i>
                </button>
            </div>
        </form>
    </div>
);

/**
 * Actions Component
 * Provides buttons for resetting the chat and refreshing the index.
 * Displays notifications based on user actions.
 */
const Actions = ({ refreshIndex, resetChat, isRefreshing, notification, setNotification }) => (
    <div className="p-6 pt-0 text-center relative">
        <div className="flex justify-center space-x-4">
            <button
                onClick={resetChat}
                className="bg-gradient-to-r from-red-100 to-red-200
                text-red-500 hover:text-white px-6 py-2 rounded-lg hover:from-red-400 hover:to-red-600 
                focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 
                transition-all duration-200 shadow-md flex items-center"
            >
                <span className="text-sm">Reset Chat</span>
                <i data-lucide="trash-2" className="w-4 h-4 ml-2"></i>
            </button>
            <button
                onClick={refreshIndex}
                className={`bg-gradient-to-r ${isRefreshing ? 'from-gray-400 to-gray-500' : 'from-green-500 to-green-600'} 
                text-white px-6 py-2 rounded-lg hover:from-green-600 hover:to-green-700 
                focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 
                disabled:opacity-50 transition-all duration-200 shadow-md flex items-center mx-auto`}
                disabled={isRefreshing} // Disable button while refreshing
            >
                <span className="text-sm">{isRefreshing ? 'Refreshing...' : 'Refresh Index'}</span>
                <i data-lucide="refresh-cw" className="w-4 h-4 ml-2"></i>
            </button>
        </div>
        {notification && (
            <div className="absolute left-1/2 transform -translate-x-1/2 mt-2">
                <Notification 
                    message={notification.message} 
                    type={notification.type}
                    onClose={() => setNotification(null)} // Allow notification to be dismissed
                />
            </div>
        )}
    </div>
);

/**
 * Footer Component
 * Displays footer information with credits and links.
 */
const Footer = () => (
    <footer className="bg-gray-100 p-6 py-4 text-center text-sm text-gray-600 border-t border-gray-200">
        <p>
            Built by 
            <a href="https://multinear.com" target="_blank" className="text-indigo-600 hover:text-indigo-800 px-1">Multinear</a>
            2024 
            <span className="text-gray-400 px-2">|</span>
            <a href="https://github.com/multinear/demo-finance-rag-llama-index" 
                target="_blank" 
                className="text-indigo-600 hover:text-indigo-800">Demo Finance RAG</a>
        </p>
    </footer>
);

/**
 * Renders the Chat component into the root DOM element.
 * Entry point of the React application.
 */
ReactDOM.render(<Chat />, document.getElementById('root'));

// Utility function to generate UUID
function generateUUID() {
    return crypto.randomUUID();
}
