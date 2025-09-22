"奇妙AI之旅" - 学生AI效率管理系统
1. 项目概述 (Overview)
开发一个面向学生群体的桌面Web应用，集成AI对话、智能记事本、任务管理和番茄钟功能。采用小清新蜡笔画风格，帮助学生提高学习效率和时间管理能力。无需注册，数据本地存储，支持多种AI模型接入。

2. 核心功能模块 (Core Modules)
🏠 首页 - AI对话界面
多模型AI对话（OpenAI、Claude、本地模型）
智能提示词推荐和管理
多媒体输入支持（文字、语音、图片、文档）
对话历史搜索和管理
📝 AI记事本
语音转文字 + 富文本编辑
AI内容分析和智能标签生成
话题分类和标签管理
记事导出功能
✅ To-Do List
多类型任务管理（今日/历史/每周/长期）
优先级设置和截止时间提醒
任务自动转移和完成率统计
独立的分类标签系统
🍅 番茄钟
心理学配色设计（蓝色工作/绿色休息）
多样化音效和背景音乐
使用统计和数据分析
自定义时长设置
3. 技术规格 (Technical Specifications)
3.1 前端架构
技术栈：Vue.js 3 + Element Plus + 小清新主题

页面布局设计：
<TEXT>
┌─────────────────────────────────────────────────────────┐
│ 🎨 奇妙AI之旅  [记事本] [To-Do] [番茄钟] [设置] ⚙️      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              🤖 AI对话界面 (首页)                        │
│  ┌─────────────────────────┬─────────────────────────┐  │
│  │ 💬 对话窗口              │ 🛠️ 功能面板              │  │
│  │ ┌─────────────────────┐ │ ┌─────────────────────┐ │  │
│  │ │ 🤖: 你好！我是你的   │ │ │ 📋 提示词库          │ │  │
│  │ │    AI学习助手        │ │ │ • 学习计划制定      │ │  │
│  │ │                     │ │ │ • 论文写作助手      │ │  │
│  │ │ 👤: 帮我制定学习计划  │ │ │ • 代码调试专家      │ │  │
│  │ └─────────────────────┘ │ │                     │ │  │
│  │                         │ │ 🏷️ 收藏的提示词      │ │  │
│  │ 💭 [输入消息...] 📎🎤📷   │ │ 📊 API使用统计       │ │  │
│  └─────────────────────────┴─────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
核心组件设计：
1. AI对话组件 (ChatInterface)

<VUE>
<template>
  <div class="chat-container crayon-style">
    <!-- 模型选择器 -->
    <div class="model-selector">
      <select v-model="selectedModel">
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
        <option value="claude-3">Claude-3</option>
        <option value="local-model">本地模型</option>
      </select>
    </div>
    
    <!-- 对话窗口 -->
    <div class="chat-messages">
      <div v-for="message in messages" 
           :class="['message', message.role]">
        <!-- 消息内容渲染 -->
      </div>
    </div>
    
    <!-- 多媒体输入区 -->
    <div class="input-area">
      <textarea v-model="inputText" 
                placeholder="输入你的问题..."></textarea>
      <div class="input-controls">
        <button @click="attachFile">📎</button>
        <button @click="startVoiceInput">🎤</button>
        <button @click="attachImage">📷</button>
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>
2. 记事本组件 (NotesInterface)

<VUE>
<template>
  <div class="notes-container crayon-style">
    <!-- 搜索和筛选 -->
    <div class="notes-header">
      <input type="text" v-model="searchQuery" 
             placeholder="🔍 搜索记事、#标签...">
      <button @click="createNote" class="btn-create">📝 新建记事</button>
      <button @click="startVoiceNote" class="btn-voice">🎤 语音记事</button>
    </div>
    
    <!-- 左侧分类栏 -->
    <div class="notes-sidebar">
      <div class="categories">
        <h3>📁 话题分类</h3>
        <div v-for="category in categories" 
             :class="['category-item', {active: selectedCategory === category.id}]"
             @click="selectCategory(category.id)">
          {{ category.icon }} {{ category.name }}
        </div>
        <button @click="createCategory">+ 新建分类</button>
      </div>
      
      <div class="tags">
        <h3>🏷️ 标签</h3>
        <div v-for="tag in tags" class="tag-item">
          #{{ tag.name }}
        </div>
      </div>
    </div>
    
    <!-- 右侧记事列表 -->
    <div class="notes-content">
      <div v-for="note in filteredNotes" class="note-card">
        <div class="note-header">
          <h4>{{ note.title }}</h4>
          <span class="note-date">{{ formatDate(note.createdAt) }}</span>
        </div>
        <div class="note-preview">{{ note.preview }}</div>
        <div class="note-tags">
          <span v-for="tag in note.tags" class="tag">#{{ tag }}</span>
        </div>
        <div class="note-ai-summary" v-if="note.aiSummary">
          🤖 AI总结：{{ note.aiSummary }}
        </div>
      </div>
    </div>
  </div>
</template>
3. 番茄钟组件 (PomodoroTimer)

<VUE>
<template>
  <div class="pomodoro-container crayon-style">
    <!-- 番茄钟主界面 -->
    <div class="timer-display" :class="timerMode">
      <div class="timer-circle">
        <svg class="progress-ring">
          <circle :stroke-dasharray="circumference"
                  :stroke-dashoffset="dashOffset"
                  class="progress-ring-circle"/>
        </svg>
        <div class="timer-text">
          <div class="time-left">{{ formattedTime }}</div>
          <div class="timer-label">{{ timerLabel }}</div>
        </div>
      </div>
      
      <!-- 控制按钮 -->
      <div class="timer-controls">
        <button @click="startTimer" v-if="!isRunning">▶️ 开始</button>
        <button @click="pauseTimer" v-if="isRunning">⏸️ 暂停</button>
        <button @click="resetTimer">🔄 重置</button>
        <button @click="skipSession">⏭️ 跳过</button>
      </div>
    </div>
    
    <!-- 设置面板 -->
    <div class="timer-settings">
      <div class="duration-settings">
        <label>工作时长: <input v-model="workDuration" type="number">分钟</label>
        <label>短休息: <input v-model="shortBreak" type="number">分钟</label>
        <label>长休息: <input v-model="longBreak" type="number">分钟</label>
      </div>
      
      <div class="sound-settings">
        <label>提醒音效:
          <select v-model="selectedSound">
            <option value="bell">铃声</option>
            <option value="chime">风铃</option>
            <option value="tick">滴答声</option>
          </select>
        </label>
        
        <label>背景音乐:
          <select v-model="backgroundMusic">
            <option value="none">无</option>
            <option value="piano">钢琴轻音乐</option>
            <option value="nature">自然白噪音</option>
            <option value="cafe">咖啡厅氛围</option>
          </select>
        </label>
      </div>
    </div>
    
    <!-- 统计面板 -->
    <div class="pomodoro-stats">
      <h3>📊 今日统计</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-number">{{ todayPomodoros }}</span>
          <span class="stat-label">完成番茄钟</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ focusTime }}</span>
          <span class="stat-label">专注时长</span>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
/* 心理学配色 */
.timer-display.work {
  background: linear-gradient(135deg, #74b9ff, #0984e3); /* 蓝色促进专注 */
}
.timer-display.break {
  background: linear-gradient(135deg, #00b894, #55a3ff); /* 绿色帮助放松 */
}
.timer-display.long-break {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe); /* 紫色深度休息 */
}
</style>
3.2 数据模型设计
AI对话数据结构：
<JAVASCRIPT>
// 对话会话
{
  id: "uuid",
  title: "学习计划讨论",
  model: "gpt-4",
  createdAt: "2024-01-15T09:00:00Z",
  updatedAt: "2024-01-15T10:30:00Z",
  messages: [
    {
      id: "msg_uuid",
      role: "user/assistant",
      content: "文本内容",
      attachments: ["file_url"], // 图片、文档等
      timestamp: "2024-01-15T09:05:00Z",
      tokenCount: 150
    }
  ],
  totalTokens: 2500,
  totalCost: 0.05
}
// 提示词模板
{
  id: "uuid",
  title: "学习计划制定助手",
  content: "你是一个专业的学习规划师...",
  category: "学习辅导",
  tags: ["学习", "计划", "时间管理"],
  isBuiltIn: true, // 内置模板
  isFavorite: false,
  usageCount: 25,
  createdAt: "2024-01-15T09:00:00Z"
}
记事本数据结构：
<JAVASCRIPT>
{
  id: "uuid",
  title: "机器学习课程笔记",
  content: "富文本内容，支持**加粗**和*斜体*",
  audioUrl: "blob:audio/recording_123.wav", // 语音记事原始文件
  transcript: "语音转文字结果",
  category: {
    id: "cat_uuid",
    name: "学习笔记",
    icon: "📚",
    color: "#74b9ff"
  },
  tags: ["机器学习", "AI", "课程"], // 用户手动+AI生成
  aiGeneratedTags: ["深度学习", "算法"], // AI建议的标签
  aiSummary: "本次学习重点是...",
  aiInsights: "建议深入学习...", // AI分析建议
  wordCount: 856,
  createdAt: "2024-01-15T14:30:00Z",
  updatedAt: "2024-01-15T15:45:00Z",
  exportHistory: [
    {
      format: "pdf",
      exportedAt: "2024-01-16T09:00:00Z"
    }
  ]
}
任务管理数据结构：
<JAVASCRIPT>
{
  id: "uuid",
  title: "完成数据结构作业",
  description: "第三章练习题1-10",
  priority: "高", // 高/中/低
  category: {
    id: "task_cat_uuid",
    name: "学习任务",
    icon: "📖",
    color: "#fd79a8"
  },
  tags: ["作业", "数据结构", "紧急"], // 任务专用标签系统
  taskType: "today", // today/history/weekly/long-term
  dueDate: "2024-01-17T23:59:00Z",
  completed: false,
  completedAt: null,
  createdAt: "2024-01-15T08:00:00Z",
  reminders: [
    {
      time: "2024-01-17T20:00:00Z",
      triggered: false
    }
  ],
  autoTransferred: false // 是否从昨日自动转移
}
番茄钟数据结构：
<JAVASCRIPT>
{
  id: "uuid",
  date: "2024-01-15",
  sessions: [
    {
      id: "session_uuid",
      type: "work/short-break/long-break",
      plannedDuration: 25, // 分钟
      actualDuration: 25,
      startTime: "2024-01-15T09:00:00Z",
      endTime: "2024-01-15T09:25:00Z",
      completed: true,
      task: "学习React", // 可选关联任务
      interruptions: 0
    }
  ],
  totalPomodoros: 6,
  totalFocusTime: 150, // 分钟
  settings: {
    workDuration: 25,
    shortBreak: 5,
    longBreak: 15,
    soundEffect: "bell",
    backgroundMusic: "piano",
    autoStartBreaks: true
  }
}
3.3 AI服务集成
API配置管理：
<JAVASCRIPT>
{
  providers: {
    openai: {
      apiKey: "encrypted_key",
      baseUrl: "https://api.openai.com/v1",
      models: ["gpt-4", "gpt-3.5-turbo"],
      enabled: true
    },
    anthropic: {
      apiKey: "encrypted_key",
      baseUrl: "https://api.anthropic.com",
      models: ["claude-3-opus", "claude-3-sonnet"],
      enabled: true
    },
    local: {
      baseUrl: "http://localhost:11434",
      models: ["llama2", "codellama"],
      enabled: false
    }
  },
  usage: {
    daily: {
      date: "2024-01-15",
      tokens: 15000,
      cost: 0.75,
      requests: 45
    },
    monthly: {
      month: "2024-01",
      tokens: 250000,
      cost: 12.50,
      requests: 650
    }
  }
}
4. 小清新蜡笔画风格设计
4.1 色彩方案
<CSS>
:root {
  /* 主色调 - 温暖柔和 */
  --primary-blue: #74b9ff;      /* 天空蓝 */
  --primary-green: #00b894;     /* 薄荷绿 */
  --primary-pink: #fd79a8;      /* 樱花粉 */
  --primary-yellow: #fdcb6e;    /* 向日葵黄 */
  
  /* 背景色 - 纸质感 */
  --bg-paper: #ffeaa7;          /* 米黄纸质 */
  --bg-white: #ffffff;
  --bg-light: #f8f9fa;
  
  /* 文字色 - 蜡笔质感 */
  --text-dark: #2d3436;         /* 深灰蜡笔 */
  --text-medium: #636e72;       /* 中灰蜡笔 */
  --text-light: #b2bec3;        /* 浅灰蜡笔 */
  
  /* 功能色 */
  --success: #00b894;           /* 成功绿 */
  --warning: #fdcb6e;           /* 警告黄 */
  --danger: #e84393;            /* 错误粉 */
  
  /* 番茄钟心理学配色 */
  --focus-blue: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  --rest-green: linear-gradient(135deg, #00b894 0%, #55efc4 100%);
  --long-rest: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
}
4.2 蜡笔画风格CSS
<CSS>
/* 全局蜡笔画风格 */
.crayon-style {
  font-family: 'Comic Sans MS', 'Marker Felt', cursive;
  background: var(--bg-paper);
  position: relative;
}
/* 手绘边框效果 */
.hand-drawn-border {
  border: 3px solid var(--primary-blue);
  border-radius: 15px;
  position: relative;
  background: white;
  box-shadow: 0 4px 15px rgba(116, 185, 255, 0.2);
}
.hand-drawn-border::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border: 2px solid var(--primary-blue);
  border-radius: 18px;
  opacity: 0.3;
  transform: rotate(-0.5deg);
}
/* 蜡笔按钮样式 */
.crayon-button {
  background: linear-gradient(45deg, var(--primary-blue), var(--primary-green));
  border: none;
  border-radius: 20px;
  padding: 12px 24px;
  color: white;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
.crayon-button:hover {
  transform: translateY(-2px) rotate(1deg);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}
/* 手绘图标 */
.crayon-icon {
  font-size: 24px;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
  transform: rotate(-2deg);
}
/* 卡片样式 */
.crayon-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 3px solid transparent;
  background-clip: padding-box;
  position: relative;
  transform: rotate(-0.5deg);
  transition: all 0.3s ease;
}
.crayon-card:hover {
  transform: rotate(0deg) translateY(-5px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
}
/* 蜡笔色彩分类 */
.category-work { border-left: 8px solid var(--primary-blue); }
.category-study { border-left: 8px solid var(--primary-green); }
.category-life { border-left: 8px solid var(--primary-pink); }
.category-idea { border-left: 8px solid var(--primary-yellow); }
4.3 小图标设计规范
HTML Artifacts
HTML
5. 开发步骤建议 (Development Steps)
第一阶段：基础架构（2-3周）
项目初始化

Vue.js 3项目搭建
小清新蜡笔画主题设计
路由和基础布局开发
数据存储系统

IndexedDB本地数据库设计
数据CRUD操作封装
数据备份恢复功能
第二阶段：AI对话模块（3-4周）
AI对话基础功能

多模型切换接口
对话界面和消息渲染
API配置和密钥管理
提示词管理系统

提示词模板库开发
收藏和分类功能
智能推荐算法
多媒体输入支持

语音输入和转文字
图片和文档上传
文件预览和处理
第三阶段：记事本模块（2-3周）
记事本核心功能

富文本编辑器集成
分类和标签系统
搜索和筛选功能
AI辅助功能

语音转文字集成
AI内容分析和总结
智能标签生成
导出功能

PDF/Word导出
批量导出选项
导出历史记录
第四阶段：任务管理模块（2周）
To-Do List开发

任务卡片组件
优先级和截止时间
任务自动转移逻辑
任务统计功能

完成率计算
任务历史记录
数据可视化
第五阶段：番茄钟模块（2-3周）
番茄钟核心功能

计时器和进度环
心理学配色实现
声音和音乐集成
番茄钟增强功能

使用统计和分析
自定义设置
通知和提醒
第六阶段：完善和优化（2周）
API管理和统计

使用量监控
费用估算
性能优化
测试和部署

功能测试
性能优化
应用打包和部署
6. 技术栈推荐
前端技术栈：
框架： Vue.js 3 + Composition API
UI库： Element Plus (自定义蜡笔画主题)
状态管理： Pinia
路由： Vue Router 4
富文本编辑： Quill.js
图表统计： Chart.js
音频处理： Web Audio API
文件处理： FileSaver.js
数据存储：
主数据库： IndexedDB (Dexie.js)
临时存储： LocalStorage
文件存储： File System Access API
AI服务集成：
OpenAI API： GPT-4, GPT-3.5-turbo
Anthropic API： Claude-3
本地模型： Ollama 接口
语音转文字： Web Speech API + OpenAI Whisper
构建和部署：
构建工具： Vite
包管理： npm
部署： Electron (桌面应用) 或 静态网站托管