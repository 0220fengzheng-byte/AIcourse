<template>
  <div class="todo-view">
    <h1 class="page-title">✅ 待办事项</h1>
    
    <FunctionNav />
    
    <div class="todo-container rainbow-card">
      <!-- 添加任务 -->
      <div class="add-task-section">
        <input 
          type="text" 
          v-model="newTask" 
          placeholder="添加新任务..." 
          class="add-task-input"
          @keyup.enter="addTask"
        >
        <button class="add-task-btn" @click="addTask" :disabled="!newTask.trim()">
          添加
        </button>
      </div>
      
      <!-- 任务过滤 -->
      <div class="task-filters">
        <button 
          v-for="filter in filters" 
          :key="filter.value" 
          :class="['filter-btn', currentFilter === filter.value ? 'active' : '']"
          @click="currentFilter = filter.value"
        >
          {{ filter.label }}
        </button>
      </div>
      
      <!-- 任务列表 -->
      <div class="tasks-list">
        <div v-if="filteredTasks.length === 0" class="empty-tasks">
          <p>{{ emptyMessage }}</p>
        </div>
        
        <div 
          v-for="task in filteredTasks" 
          :key="task.id"
          :class="['task-item', task.completed ? 'completed' : '']"
        >
          <div class="task-checkbox">
            <input 
              type="checkbox" 
              :checked="task.completed"
              @change="toggleTask(task)"
            >
          </div>
          
          <div class="task-content">
            <div class="task-text">{{ task.text }}</div>
            <div class="task-date">{{ formatDate(task.createdAt) }}</div>
          </div>
          
          <div class="task-actions">
            <button class="delete-btn" @click="deleteTask(task)">
              🗑️
            </button>
          </div>
        </div>
      </div>
      
      <!-- 任务统计 -->
      <div class="task-stats">
        <div class="stats-item">
          <span>总任务:</span> {{ tasks.length }}
        </div>
        <div class="stats-item">
          <span>已完成:</span> {{ completedCount }}
        </div>
        <div class="stats-item">
          <span>未完成:</span> {{ pendingCount }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import FunctionNav from '@/components/ui/FunctionNav.vue'

export default {
  name: 'TodoView',
  components: {
    FunctionNav
  },
  
  setup() {
    const tasks = ref([])
    const newTask = ref('')
    const currentFilter = ref('all')
    
    const filters = [
      { label: '全部', value: 'all' },
      { label: '未完成', value: 'pending' },
      { label: '已完成', value: 'completed' }
    ]
    
    // 从本地存储加载任务
    const loadTasks = () => {
      const savedTasks = localStorage.getItem('tasks')
      if (savedTasks) {
        tasks.value = JSON.parse(savedTasks)
      }
    }
    
    // 保存任务到本地存储
    const saveTasks = () => {
      localStorage.setItem('tasks', JSON.stringify(tasks.value))
    }
    
    // 添加新任务
    const addTask = () => {
      if (!newTask.value.trim()) return
      
      const task = {
        id: Date.now().toString(),
        text: newTask.value,
        completed: false,
        createdAt: new Date()
      }
      
      tasks.value.unshift(task)
      saveTasks()
      newTask.value = ''
    }
    
    // 切换任务状态
    const toggleTask = (task) => {
      task.completed = !task.completed
      saveTasks()
    }
    
    // 删除任务
    const deleteTask = (task) => {
      tasks.value = tasks.value.filter(t => t.id !== task.id)
      saveTasks()
    }
    
    // 过滤任务
    const filteredTasks = computed(() => {
      switch (currentFilter.value) {
        case 'pending':
          return tasks.value.filter(task => !task.completed)
        case 'completed':
          return tasks.value.filter(task => task.completed)
        default:
          return tasks.value
      }
    })
    
    // 空状态消息
    const emptyMessage = computed(() => {
      switch (currentFilter.value) {
        case 'pending':
          return '没有未完成的任务'
        case 'completed':
          return '没有已完成的任务'
        default:
          return '没有任务，添加一个吧！'
      }
    })
    
    // 任务统计
    const completedCount = computed(() => {
      return tasks.value.filter(task => task.completed).length
    })
    
    const pendingCount = computed(() => {
      return tasks.value.filter(task => !task.completed).length
    })
    
    // 格式化日期
    const formatDate = (date) => {
      const d = new Date(date)
      return d.toLocaleDateString()
    }
    
    onMounted(() => {
      loadTasks()
    })
    
    return {
      tasks,
      newTask,
      currentFilter,
      filters,
      filteredTasks,
      emptyMessage,
      completedCount,
      pendingCount,
      addTask,
      toggleTask,
      deleteTask,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.todo-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .todo-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }
  
  .add-task-section {
    display: flex;
    gap: 0.5rem;
    
    .add-task-input {
      flex: 1;
      padding: 0.75rem 1rem;
      border: 1px solid var(--text-light);
      border-radius: 0.5rem;
      font-size: 1rem;
      
      &:focus {
        outline: none;
        border-color: var(--primary-green);
      }
    }
    
    .add-task-btn {
      background-color: var(--primary-green);
      color: white;
      border: none;
      border-radius: 0.5rem;
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.2s;
      
      &:hover {
        background-color: darken(#00b894, 10%);
      }
      
      &:disabled {
        background-color: var(--text-light);
        cursor: not-allowed;
      }
    }
  }
  
  .task-filters {
    display: flex;
    gap: 0.5rem;
    
    .filter-btn {
      background-color: var(--bg-light);
      border: none;
      border-radius: 0.5rem;
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s;
      
      &:hover {
        background-color: darken(#f8f9fa, 5%);
      }
      
      &.active {
        background-color: var(--primary-green);
        color: white;
      }
    }
  }
  
  .tasks-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 50vh;
    overflow-y: auto;
    padding: 0.5rem;
    
    .empty-tasks {
      text-align: center;
      padding: 2rem;
      color: var(--text-medium);
    }
    
    .task-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
      background-color: white;
      border-radius: 0.5rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      transition: all 0.2s;
      
      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }
      
      &.completed {
        .task-text {
          text-decoration: line-through;
          color: var(--text-light);
        }
      }
      
      .task-checkbox {
        input[type="checkbox"] {
          width: 20px;
          height: 20px;
          cursor: pointer;
        }
      }
      
      .task-content {
        flex: 1;
        
        .task-text {
          margin-bottom: 0.25rem;
          color: var(--text-dark);
        }
        
        .task-date {
          font-size: 0.8rem;
          color: var(--text-light);
        }
      }
      
      .task-actions {
        .delete-btn {
          background: none;
          border: none;
          font-size: 1.2rem;
          cursor: pointer;
          opacity: 0.5;
          transition: opacity 0.2s;
          
          &:hover {
            opacity: 1;
          }
        }
      }
    }
  }
  
  .task-stats {
    display: flex;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid var(--text-light);
    
    .stats-item {
      font-size: 0.9rem;
      color: var(--text-medium);
      
      span {
        font-weight: bold;
        margin-right: 0.25rem;
      }
    }
  }
}
</style>