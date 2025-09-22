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

      <!-- 任务类型和优先级选择 -->
      <div class="task-options">
        <div class="task-category">
          <label>任务类型:</label>
          <select v-model="newTaskCategory" class="category-select">
            <option value="today">今日任务</option>
            <option value="week">本周任务</option>
            <option value="longterm">长期任务</option>
          </select>
        </div>

        <div class="task-priority">
          <label>优先级:</label>
          <select v-model="newTaskPriority" class="priority-select">
            <option value="high">高</option>
            <option value="medium">中</option>
            <option value="low">低</option>
          </select>
        </div>
      </div>

      <!-- 任务分类标签 -->
      <div class="task-category-tabs">
        <button
          v-for="category in categories"
          :key="category.value"
          :class="['category-tab', currentCategory === category.value ? 'active' : '', category.class]"
          @click="currentCategory = category.value"
        >
          {{ category.label }} ({{ getCategoryCount(category.value) }})
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
          :class="['task-item', task.completed ? 'completed' : '', getPriorityClass(task.priority)]"
        >
          <div class="task-checkbox">
            <input
              type="checkbox"
              :checked="task.completed"
              @change="toggleTask(task)"
            >
          </div>

          <div class="task-content">
            <div class="task-header">
              <div class="task-text">{{ task.text }}</div>
              <div class="task-badges">
                <span :class="['priority-badge', getPriorityClass(task.priority)]">{{ getPriorityText(task.priority) }}</span>
                <span :class="['category-badge', getCategoryClass(task.category)]">{{ getCategoryText(task.category) }}</span>
              </div>
            </div>
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
    const newTaskCategory = ref('today')
    const newTaskPriority = ref('medium')
    const currentFilter = ref('all')
    const currentCategory = ref('all')

    const filters = [
      { label: '全部', value: 'all' },
      { label: '未完成', value: 'pending' },
      { label: '已完成', value: 'completed' }
    ]

    const categories = [
      { label: '全部任务', value: 'all', class: 'all-tasks' },
      { label: '今日任务', value: 'today', class: 'today-tasks' },
      { label: '本周任务', value: 'week', class: 'week-tasks' },
      { label: '长期任务', value: 'longterm', class: 'longterm-tasks' },
      { label: '历史任务', value: 'history', class: 'history-tasks' }
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
        category: newTaskCategory.value,
        priority: newTaskPriority.value,
        createdAt: new Date(),
        completedAt: null
      }

      tasks.value.unshift(task)
      saveTasks()
      newTask.value = ''
    }

    // 切换任务状态
    const toggleTask = (task) => {
      task.completed = !task.completed
      if (task.completed) {
        task.completedAt = new Date()
      } else {
        task.completedAt = null
      }
      saveTasks()
    }

    // 删除任务
    const deleteTask = (task) => {
      tasks.value = tasks.value.filter(t => t.id !== task.id)
      saveTasks()
    }

    // 获取优先级类名
    const getPriorityClass = (priority) => {
      return `priority-${priority}`
    }

    // 获取优先级文本
    const getPriorityText = (priority) => {
      const priorityMap = {
        high: '高',
        medium: '中',
        low: '低'
      }
      return priorityMap[priority] || '中'
    }

    // 获取分类类名
    const getCategoryClass = (category) => {
      return `category-${category}`
    }

    // 获取分类文本
    const getCategoryText = (category) => {
      const categoryMap = {
        today: '今日',
        week: '本周',
        longterm: '长期',
        history: '历史'
      }
      return categoryMap[category] || '今日'
    }

    // 获取分类数量
    const getCategoryCount = (category) => {
      if (category === 'all') return tasks.value.length
      if (category === 'history') return tasks.value.filter(task => task.completed).length
      return tasks.value.filter(task => task.category === category && !task.completed).length
    }

    // 检查任务是否在本周内
    const isInCurrentWeek = (date) => {
      const taskDate = new Date(date)
      const now = new Date()
      const startOfWeek = new Date(now.setDate(now.getDate() - now.getDay()))
      const endOfWeek = new Date(now.setDate(now.getDate() - now.getDay() + 6))
      return taskDate >= startOfWeek && taskDate <= endOfWeek
    }

    // 检查任务是否是今日任务
    const isToday = (date) => {
      const taskDate = new Date(date)
      const today = new Date()
      return taskDate.toDateString() === today.toDateString()
    }

    // 过滤任务
    const filteredTasks = computed(() => {
      let filtered = tasks.value

      // 按分类过滤
      if (currentCategory.value !== 'all') {
        if (currentCategory.value === 'history') {
          filtered = filtered.filter(task => task.completed)
        } else {
          filtered = filtered.filter(task => {
            if (task.category === 'today') return isToday(task.createdAt) && !task.completed
            if (task.category === 'week') return isInCurrentWeek(task.createdAt) && !task.completed
            if (task.category === 'longterm') return task.category === 'longterm' && !task.completed
            return true
          })
        }
      }

      // 按状态过滤
      switch (currentFilter.value) {
        case 'pending':
          return filtered.filter(task => !task.completed)
        case 'completed':
          return filtered.filter(task => task.completed)
        default:
          return filtered
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
      newTaskCategory,
      newTaskPriority,
      currentFilter,
      currentCategory,
      filters,
      categories,
      filteredTasks,
      emptyMessage,
      completedCount,
      pendingCount,
      addTask,
      toggleTask,
      deleteTask,
      formatDate,
      getPriorityClass,
      getPriorityText,
      getCategoryClass,
      getCategoryText,
      getCategoryCount
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

  .task-options {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background-color: var(--bg-light);
    border-radius: 0.5rem;

    .task-category, .task-priority {
      display: flex;
      align-items: center;
      gap: 0.5rem;

      label {
        font-weight: bold;
        color: var(--text-dark);
        font-size: 0.9rem;
      }

      select {
        padding: 0.5rem;
        border: 1px solid var(--text-light);
        border-radius: 0.25rem;
        background-color: white;
        font-size: 0.9rem;

        &:focus {
          outline: none;
          border-color: var(--primary-green);
        }
      }
    }
  }

  .task-category-tabs {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem;
    background-color: var(--bg-light);
    border-radius: 0.5rem;
    flex-wrap: wrap;

    .category-tab {
      background-color: white;
      border: 1px solid var(--text-light);
      border-radius: 0.5rem;
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        background-color: darken(#f8f9fa, 5%);
      }

      &.active {
        color: white;
        font-weight: bold;

        &.all-tasks {
          background-color: var(--primary-blue);
          border-color: var(--primary-blue);
        }

        &.today-tasks {
          background-color: #ff6b6b;
          border-color: #ff6b6b;
        }

        &.week-tasks {
          background-color: #4ecdc4;
          border-color: #4ecdc4;
        }

        &.longterm-tasks {
          background-color: #45b7d1;
          border-color: #45b7d1;
        }

        &.history-tasks {
          background-color: #96ceb4;
          border-color: #96ceb4;
        }
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
      border-left: 4px solid transparent;

      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      // 优先级颜色编码
      &.priority-high {
        border-left-color: #ff4757;

        .task-header {
          .task-text {
            color: #ff4757;
            font-weight: bold;
          }
        }
      }

      &.priority-medium {
        border-left-color: #ffa502;
      }

      &.priority-low {
        border-left-color: #2ed573;
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

        .task-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.5rem;

          .task-text {
            flex: 1;
            margin-right: 1rem;
            color: var(--text-dark);
          }

          .task-badges {
            display: flex;
            gap: 0.5rem;
            flex-shrink: 0;

            .priority-badge, .category-badge {
              padding: 0.25rem 0.5rem;
              border-radius: 0.25rem;
              font-size: 0.75rem;
              font-weight: bold;
              color: white;
            }

            .priority-badge {
              &.priority-high {
                background-color: #ff4757;
              }

              &.priority-medium {
                background-color: #ffa502;
              }

              &.priority-low {
                background-color: #2ed573;
              }
            }

            .category-badge {
              &.category-today {
                background-color: #ff6b6b;
              }

              &.category-week {
                background-color: #4ecdc4;
              }

              &.category-longterm {
                background-color: #45b7d1;
              }
            }
          }
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