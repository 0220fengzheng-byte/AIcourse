<template>
  <div class="pomodoro-view">
    <h1 class="page-title">🍅 番茄钟</h1>
    
    <FunctionNav />
    
    <div class="pomodoro-container rainbow-card">
      <!-- 计时器显示 -->
      <div class="timer-display">
        <div class="timer-circle" :class="{ 'active': isActive, 'break': isBreak }">
          <div class="timer-text">{{ formattedTime }}</div>
          <div class="timer-mode">{{ currentMode }}</div>
        </div>
      </div>
      
      <!-- 控制按钮 -->
      <div class="timer-controls">
        <button 
          class="control-btn" 
          @click="toggleTimer"
          :class="{ 'start': !isActive, 'stop': isActive }"
        >
          {{ isActive ? '暂停' : '开始' }}
        </button>
        
        <button 
          class="control-btn reset" 
          @click="resetTimer"
          :disabled="!canReset"
        >
          重置
        </button>
      </div>
      
      <!-- 设置 -->
      <div class="timer-settings">
        <h3>设置</h3>
        
        <div class="settings-group">
          <div class="setting-item">
            <label>工作时间 (分钟)</label>
            <input 
              type="number" 
              v-model.number="workDuration" 
              min="1" 
              max="60"
              :disabled="isActive"
            >
          </div>
          
          <div class="setting-item">
            <label>休息时间 (分钟)</label>
            <input 
              type="number" 
              v-model.number="breakDuration" 
              min="1" 
              max="30"
              :disabled="isActive"
            >
          </div>
        </div>
      </div>
      
      <!-- 统计信息 -->
      <div class="timer-stats">
        <div class="stats-item">
          <div class="stats-label">今日完成</div>
          <div class="stats-value">{{ completedToday }}</div>
        </div>
        
        <div class="stats-item">
          <div class="stats-label">总计完成</div>
          <div class="stats-value">{{ completedTotal }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import FunctionNav from '@/components/ui/FunctionNav.vue'

export default {
  name: 'PomodoroView',
  components: {
    FunctionNav
  },
  
  setup() {
    // 状态变量
    const isActive = ref(false)
    const isBreak = ref(false)
    const timeLeft = ref(0)
    const workDuration = ref(25)
    const breakDuration = ref(5)
    const completedToday = ref(0)
    const completedTotal = ref(0)
    const timerInterval = ref(null)
    
    // 计算属性
    const formattedTime = computed(() => {
      const minutes = Math.floor(timeLeft.value / 60)
      const seconds = timeLeft.value % 60
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    })
    
    const currentMode = computed(() => {
      return isBreak.value ? '休息时间' : '工作时间'
    })
    
    const canReset = computed(() => {
      return isActive.value || timeLeft.value !== workDuration.value * 60
    })
    
    // 方法
    const startTimer = () => {
      if (!isActive.value) {
        isActive.value = true
        timerInterval.value = setInterval(() => {
          if (timeLeft.value > 0) {
            timeLeft.value--
          } else {
            // 时间结束，切换模式
            playAlarm()
            if (!isBreak.value) {
              // 工作时间结束，切换到休息时间
              isBreak.value = true
              timeLeft.value = breakDuration.value * 60
              completedToday.value++
              completedTotal.value++
              saveStats()
              showNotification('工作时间结束', '休息一下吧！')
            } else {
              // 休息时间结束，切换到工作时间
              isBreak.value = false
              timeLeft.value = workDuration.value * 60
              showNotification('休息时间结束', '开始新的工作吧！')
            }
          }
        }, 1000)
      }
    }
    
    const stopTimer = () => {
      if (isActive.value) {
        isActive.value = false
        clearInterval(timerInterval.value)
      }
    }
    
    const toggleTimer = () => {
      if (isActive.value) {
        stopTimer()
      } else {
        startTimer()
      }
    }
    
    const resetTimer = () => {
      stopTimer()
      isBreak.value = false
      timeLeft.value = workDuration.value * 60
    }
    
    const playAlarm = () => {
      try {
        const audio = new Audio('/alarm.mp3')
        audio.play()
      } catch (error) {
        console.error('无法播放提示音', error)
      }
    }
    
    const showNotification = (title, body) => {
      if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification(title, { body })
          }
        })
      }
    }
    
    // 保存和加载统计数据
    const saveStats = () => {
      const stats = {
        completedToday,
        completedTotal: completedTotal.value,
        lastDate: new Date().toDateString()
      }
      localStorage.setItem('pomodoroStats', JSON.stringify(stats))
    }
    
    const loadStats = () => {
      const savedStats = localStorage.getItem('pomodoroStats')
      if (savedStats) {
        const stats = JSON.parse(savedStats)
        completedTotal.value = stats.completedTotal || 0
        
        // 检查是否是今天
        const today = new Date().toDateString()
        if (stats.lastDate === today) {
          completedToday.value = stats.completedToday || 0
        } else {
          completedToday.value = 0
          saveStats()
        }
      }
    }
    
    // 监听设置变化
    watch(workDuration, (newVal) => {
      if (!isActive.value && !isBreak.value) {
        timeLeft.value = newVal * 60
      }
    })
    
    // 生命周期钩子
    onMounted(() => {
      loadStats()
      timeLeft.value = workDuration.value * 60
    })
    
    onBeforeUnmount(() => {
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }
    })
    
    return {
      isActive,
      isBreak,
      timeLeft,
      workDuration,
      breakDuration,
      completedToday,
      completedTotal,
      formattedTime,
      currentMode,
      canReset,
      toggleTimer,
      resetTimer
    }
  }
}
</script>

<style lang="scss" scoped>
.pomodoro-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .pomodoro-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
    align-items: center;
  }
  
  .timer-display {
    display: flex;
    justify-content: center;
    
    .timer-circle {
      width: 250px;
      height: 250px;
      border-radius: 50%;
      background-color: var(--bg-light);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      border: 8px solid var(--primary-green);
      
      &.active {
        animation: pulse 2s infinite;
      }
      
      &.break {
        border-color: var(--primary-blue);
      }
      
      .timer-text {
        font-size: 3.5rem;
        font-weight: bold;
        color: var(--text-dark);
      }
      
      .timer-mode {
        font-size: 1.2rem;
        color: var(--text-medium);
        margin-top: 0.5rem;
      }
    }
  }
  
  .timer-controls {
    display: flex;
    gap: 1rem;
    
    .control-btn {
      padding: 0.75rem 2rem;
      border: none;
      border-radius: 2rem;
      font-size: 1.1rem;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.2s;
      
      &.start {
        background-color: var(--primary-green);
        color: white;
        
        &:hover {
          background-color: darken(#00b894, 10%);
        }
      }
      
      &.stop {
        background-color: var(--primary-red);
        color: white;
        
        &:hover {
          background-color: darken(#e74c3c, 10%);
        }
      }
      
      &.reset {
        background-color: var(--bg-light);
        color: var(--text-dark);
        
        &:hover {
          background-color: darken(#f8f9fa, 5%);
        }
        
        &:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      }
    }
  }
  
  .timer-settings {
    width: 100%;
    max-width: 500px;
    
    h3 {
      margin-bottom: 1rem;
      color: var(--text-dark);
    }
    
    .settings-group {
      display: flex;
      gap: 1.5rem;
      
      .setting-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        
        label {
          font-size: 0.9rem;
          color: var(--text-medium);
        }
        
        input {
          padding: 0.75rem;
          border: 1px solid var(--text-light);
          border-radius: 0.5rem;
          font-size: 1rem;
          
          &:focus {
            outline: none;
            border-color: var(--primary-green);
          }
          
          &:disabled {
            background-color: var(--bg-light);
            cursor: not-allowed;
          }
        }
      }
    }
  }
  
  .timer-stats {
    display: flex;
    gap: 3rem;
    
    .stats-item {
      text-align: center;
      
      .stats-label {
        font-size: 0.9rem;
        color: var(--text-medium);
        margin-bottom: 0.25rem;
      }
      
      .stats-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-green);
      }
    }
  }
  
  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.02);
    }
    100% {
      transform: scale(1);
    }
  }
}
</style>