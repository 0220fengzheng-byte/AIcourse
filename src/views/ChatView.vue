<template>
  <div class="chat-view">
    <h1 class="page-title">🤖 AI对话</h1>
    
    <FunctionNav />
    
    <div class="model-selection">
      <label for="model-select">选择模型：</label>
      <select id="model-select" v-model="selectedModel" class="model-select">
        <option v-for="model in availableModels" :key="model.id" :value="model.id">
          {{ model.name }}
        </option>
      </select>
      <div class="api-key-info" v-if="!apiKey">
        <span class="api-key-notice">请在<router-link to="/settings" class="settings-link">设置</router-link>中配置API Key</span>
      </div>
    </div>
    
    <div class="chat-container rainbow-card">
      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-indicator">
          <div class="loading-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
        </div>
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
          <div class="message-avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="chat-input-area">
        <textarea 
          v-model="userInput" 
          class="chat-input" 
          placeholder="输入你的问题..." 
          @keydown.enter.prevent="sendMessage"
        ></textarea>
        <div class="input-actions">
          <button class="send-button" @click="sendMessage" :disabled="!userInput.trim()">
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useAIStore } from '@/stores/aiStore'
import { storeToRefs } from 'pinia'
import FunctionNav from '@/components/ui/FunctionNav.vue'

export default {
  name: 'ChatView',
  components: {
    FunctionNav
  },
  
  setup() {
    const userInput = ref('')
    const messages = ref([
      {
        role: 'ai',
        content: '你好！我是你的AI学习助手。有什么我可以帮助你的吗？',
        timestamp: new Date()
      }
    ])
    const messagesContainer = ref(null)
    const isLoading = ref(false)
    
    // 使用AI Store
    const aiStore = useAIStore()
    const { apiKey, selectedModel, availableModels } = storeToRefs(aiStore)
    
    // 发送消息
    const sendMessage = async () => {
      if (!userInput.value.trim()) return
      
      // 添加用户消息
      const userMessage = {
        role: 'user',
        content: userInput.value,
        timestamp: new Date()
      }
      messages.value.push(userMessage)
      userInput.value = ''
      
      // 滚动到底部
      await nextTick()
      scrollToBottom()
      
      // 添加加载中的消息
      isLoading.value = true
      
      try {
        // 如果有API Key，使用OpenRouter API
        if (apiKey.value) {
          const aiResponse = {
            role: 'ai',
            content: await getAIResponseFromAPI(userMessage.content),
            timestamp: new Date()
          }
          messages.value.push(aiResponse)
        } else {
          // 否则使用模拟回复
          const aiResponse = {
            role: 'ai',
            content: getAIResponse(),
            timestamp: new Date()
          }
          messages.value.push(aiResponse)
        }
      } catch (error) {
        // 处理错误
        const errorMessage = {
          role: 'ai',
          content: `发生错误: ${error.message || '请检查API Key是否正确'}`,
          timestamp: new Date()
        }
        messages.value.push(errorMessage)
      } finally {
        isLoading.value = false
        // 滚动到底部
        nextTick(() => scrollToBottom())
      }
    }
    
    // 格式化时间
    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    // 滚动到底部
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    // 监听消息变化，自动滚动
    watch(() => messages.value.length, () => {
      nextTick(() => scrollToBottom())
    })
    
    // 模拟AI回复
    const getAIResponse = () => {
      const responses = [
        '我理解你的问题，让我思考一下...',
        '这是一个很好的问题！',
        '根据我的理解，这个问题的答案是...',
        '我可以帮你解决这个问题。',
        '这个问题有点复杂，让我详细解释一下。',
        '我需要更多信息来回答这个问题。',
        '你可以尝试这样做...',
        '我建议你考虑以下几点...',
      ]
      return responses[Math.floor(Math.random() * responses.length)]
    }
    
    // 使用OpenRouter API获取AI回复
    const getAIResponseFromAPI = async (userMessage) => {
      try {
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey.value}`,
            'HTTP-Referer': window.location.origin,
          },
          body: JSON.stringify({
            model: selectedModel.value,
            messages: [
              {
                role: 'user',
                content: userMessage
              }
            ],
            max_tokens: 1000
          })
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error?.message || '请求失败')
        }
        
        const data = await response.json()
        return data.choices[0]?.message?.content || '无法获取回复'
      } catch (error) {
        console.error('API请求错误:', error)
        throw error
      }
    }
    
    onMounted(() => {
      scrollToBottom()
    })
    
    return {
      userInput,
      messages,
      messagesContainer,
      sendMessage,
      formatTime,
      apiKey,
      selectedModel,
      availableModels,
      isLoading
    }
  }
}
</script>

<style lang="scss" scoped>
.chat-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .model-selection {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    
    label {
      font-weight: 500;
      color: var(--text-dark);
    }
    
    .model-select {
      padding: 0.5rem;
      border-radius: 0.5rem;
      border: 1px solid var(--text-light);
      background-color: var(--bg-light);
      min-width: 200px;
      
      &:focus {
        outline: none;
        border-color: var(--primary-blue);
      }
    }
    
    .api-key-info {
      flex: 1;
      
      .api-key-notice {
        color: var(--text-medium);
        font-size: 0.9rem;
      }
      
      .settings-link {
        color: var(--primary-blue);
        text-decoration: none;
        font-weight: 500;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
  
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 70vh;
    overflow: hidden;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    
    .loading-indicator {
      align-self: flex-start;
      margin-bottom: 1rem;
      
      .loading-dots {
        display: flex;
        gap: 0.5rem;
        
        .dot {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background-color: var(--primary-blue);
          opacity: 0.6;
          animation: pulse 1.5s infinite ease-in-out;
          
          &:nth-child(2) {
            animation-delay: 0.2s;
          }
          
          &:nth-child(3) {
            animation-delay: 0.4s;
          }
        }
      }
    }
    
    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
        opacity: 0.6;
      }
      50% {
        transform: scale(1.2);
        opacity: 1;
      }
    }
    
    .message {
      display: flex;
      gap: 1rem;
      max-width: 80%;
      
      &.user-message {
        align-self: flex-end;
        flex-direction: row-reverse;
        
        .message-content {
          background-color: var(--primary-blue);
          color: white;
          border-radius: 1rem 0 1rem 1rem;
        }
      }
      
      &.ai-message {
        align-self: flex-start;
        
        .message-content {
          background-color: var(--bg-light);
          border-radius: 0 1rem 1rem 1rem;
        }
      }
      
      .message-avatar {
        font-size: 1.5rem;
        display: flex;
        align-items: flex-end;
      }
      
      .message-content {
        padding: 1rem;
        
        .message-text {
          margin-bottom: 0.5rem;
          white-space: pre-wrap;
        }
        
        .message-time {
          font-size: 0.8rem;
          opacity: 0.7;
          text-align: right;
        }
      }
    }
  }
  
  .chat-input-area {
    border-top: 1px solid var(--text-light);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    
    .chat-input {
      width: 100%;
      min-height: 80px;
      padding: 0.75rem;
      border: 1px solid var(--text-light);
      border-radius: 0.5rem;
      resize: none;
      font-family: inherit;
      font-size: 1rem;
      
      &:focus {
        outline: none;
        border-color: var(--primary-blue);
      }
    }
    
    .input-actions {
      display: flex;
      justify-content: flex-end;
      
      .send-button {
        background-color: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s;
        
        &:hover {
          background-color: darken(#74b9ff, 10%);
        }
        
        &:disabled {
          background-color: var(--text-light);
          cursor: not-allowed;
        }
      }
    }
  }
}
</style>