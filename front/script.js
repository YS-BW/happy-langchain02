// DOM 元素引用
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatContainer = document.getElementById('chat-container');
const welcomeMessage = document.getElementById('welcome-message');

// API 接口地址 (注意：如果前端和后端不是在同一个域名/端口，需要修改为完整的 URL)
const API_URL = '/chat-stream'; 

// 启用/禁用发送按钮
chatInput.addEventListener('input', () => {
    sendButton.disabled = chatInput.value.trim() === '';
});

// 监听发送按钮点击和回车键
sendButton.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !sendButton.disabled) {
        sendMessage();
    }
});


/**
 * 滚动聊天容器到底部
 */
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * 创建并添加一个新的聊天气泡
 * @param {string} role - 'user' 或 'ai'
 * @param {string} content - 聊天内容
 * @returns {HTMLElement} 新创建的气泡元素
 */
function addMessage(role, content = '') {
    // 移除欢迎界面
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
        welcomeMessage.remove(); // 彻底移除，避免占位
    }

    const messageElement = document.createElement('div');
    messageElement.classList.add('flex', 'mb-6', 'animate-fade-in'); // 使用动画类

    if (role === 'user') {
        messageElement.innerHTML = `
            <img class="w-8 h-8 rounded-full mr-3 mt-1" src="https://via.placeholder.com/150/1a73e8/ffffff?text=U" alt="User">
            <div class="max-w-xl bg-gemini-input text-gray-800 p-3 rounded-2xl rounded-tl-none shadow-sm">
                <p>${content}</p>
            </div>
        `;
    } else if (role === 'ai') {
        // AI 消息气泡，初始内容为空，用于接收流
        messageElement.innerHTML = `
            <div class="flex-shrink-0 w-8 h-8 mr-3 mt-1 flex items-center justify-center bg-gemini-blue rounded-full">
                 <div class="w-2 h-2 bg-white transform rotate-45"></div>
            </div>
            <div class="max-w-xl bg-white text-gray-800 p-3 rounded-2xl rounded-tl-none shadow border border-gray-100">
                <p id="ai-response-${Date.now()}" class="ai-typing-area whitespace-pre-wrap"></p>
            </div>
        `;
    }
    
    chatContainer.appendChild(messageElement);
    scrollToBottom();
    
    // 返回 AI 消息的文本区域元素，方便后续流式写入
    return role === 'ai' ? messageElement.querySelector('.ai-typing-area') : null;
}

/**
 * 发送用户消息并处理 AI 流式响应
 */
async function sendMessage() {
    const question = chatInput.value.trim();
    if (!question) return;

    // 1. 添加用户消息气泡
    addMessage('user', question);

    // 2. 清空输入框并禁用
    chatInput.value = '';
    sendButton.disabled = true;
    chatInput.disabled = true;

    // 3. 添加 AI 消息占位符并获取接收文本区域
    const aiResponseArea = addMessage('ai');
    
    try {
        // 4. 发送请求
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // 匹配您后端的 ChatRequest 结构
            body: JSON.stringify({ question: question }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 5. 处理流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let fullResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            // 解码并附加 chunk
            const chunk = decoder.decode(value, { stream: true });
            fullResponse += chunk;
            
            // 模拟打字机效果：每次接收到数据就更新 DOM
            aiResponseArea.innerHTML = fullResponse;

            // 保持滚动到底部
            scrollToBottom();
        }

    } catch (error) {
        console.error('Stream chat failed:', error);
        // 显示错误信息
        aiResponseArea.innerHTML = `<span class="text-red-500">❌ 连接失败或服务器错误: ${error.message}</span>`;
    } finally {
        // 6. 重新启用输入框和按钮
        chatInput.disabled = false;
        sendButton.disabled = chatInput.value.trim() === '';
        chatInput.focus();
    }
}