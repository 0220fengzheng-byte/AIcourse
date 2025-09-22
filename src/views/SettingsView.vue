<template>
  <div class="settings-view">
    <h1 class="page-title">⚙️ 设置</h1>
    
    <div class="settings-container rainbow-card">
      <h2 class="settings-section-title">AI对话设置</h2>
      
      <div class="settings-section">
        <div class="setting-item">
          <label for="api-key">OpenRouter API Key</label>
          <input 
            id="api-key"
            v-model="apiKey" 
            type="password" 
            placeholder="输入OpenRouter API Key" 
            class="api-key-input"
          />
          <p class="setting-description">用于访问OpenRouter API的密钥，可以在OpenRouter网站获取</p>
        </div>
        
        <div class="setting-item">
          <label for="model-select">默认AI模型</label>
          <select id="model-select" v-model="selectedModel" class="model-select">
            <option v-for="model in availableModels" :key="model.id" :value="model.id">
              {{ model.name }}
            </option>
          </select>
          <p class="setting-description">在AI对话中默认使用的大语言模型</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAIStore } from '@/stores/aiStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'SettingsView',
  
  setup() {
    const aiStore = useAIStore()
    const { apiKey, selectedModel, availableModels } = storeToRefs(aiStore)
    
    return {
      apiKey,
      selectedModel,
      availableModels
    }
  }
}
</script>

<style lang="scss" scoped>
.settings-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .settings-container {
    padding: 2rem;
    
    .settings-section-title {
      font-size: 1.5rem;
      color: var(--text-dark);
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--text-light);
      padding-bottom: 0.5rem;
    }
    
    .settings-section {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      
      .setting-item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        
        label {
          font-weight: 500;
          color: var(--text-dark);
        }
        
        .api-key-input, .model-select {
          padding: 0.75rem;
          border-radius: 0.5rem;
          border: 1px solid var(--text-light);
          font-size: 1rem;
          width: 100%;
          max-width: 500px;
          
          &:focus {
            outline: none;
            border-color: var(--primary-blue);
          }
        }
        
        .setting-description {
          color: var(--text-medium);
          font-size: 0.9rem;
          margin-top: 0.25rem;
        }
      }
    }
  }
}
</style>