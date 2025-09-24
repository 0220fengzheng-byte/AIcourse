import { defineStore } from 'pinia'

export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: [
      {
        id: 1,
        name: '设计团队任务管理系统UI',
        description: '设计一套小清新风格的团队任务管理系统UI，包括任务列表、任务详情、新建任务等页面。',
        type: '设计',
        status: '已完成',
        priority: '高',
        assignee: 1,
        dueDate: '2023-06-15',
        createdAt: '2023-06-01T08:00:00.000Z',
        documentLink: 'https://feishu.cn/docx/design-system-ui',
        hasAttachments: true,
        attachments: [
          {
            name: 'UI设计稿.sketch',
            size: 2048000,
            type: 'application/octet-stream'
          }
        ]
      },
      {
        id: 2,
        name: '实现任务列表组件',
        description: '使用Vue 3和Element Plus实现任务列表组件，包括筛选、排序和分页功能。',
        type: '开发',
        status: '进行中',
        priority: '高',
        assignee: 2,
        dueDate: '2023-06-20',
        createdAt: '2023-06-05T09:30:00.000Z',
        documentLink: 'https://docs.google.com/document/d/123456789',
        hasAttachments: false,
        attachments: []
      },
      {
        id: 3,
        name: '编写API接口文档',
        description: '编写团队任务管理系统的API接口文档，包括任务的增删改查等接口。',
        type: '文档',
        status: '未开始',
        priority: '中',
        assignee: 3,
        dueDate: '2023-06-25',
        createdAt: '2023-06-10T14:00:00.000Z',
        documentLink: 'https://yuque.com/api-docs/task-management',
        hasAttachments: false,
        attachments: []
      },
      {
        id: 4,
        name: '实现任务详情页面',
        description: '开发任务详情页面，展示任务的详细信息，包括描述、状态、优先级、负责人等。',
        type: '开发',
        status: '未开始',
        priority: '中',
        assignee: 2,
        dueDate: '2023-06-30',
        createdAt: '2023-06-12T11:20:00.000Z',
        hasAttachments: false,
        attachments: []
      },
      {
        id: 5,
        name: '测试任务管理功能',
        description: '对团队任务管理系统进行功能测试，包括任务的创建、编辑、删除、状态变更等操作。',
        type: '测试',
        status: '未开始',
        priority: '低',
        assignee: 4,
        dueDate: '2023-07-05',
        createdAt: '2023-06-15T16:45:00.000Z',
        hasAttachments: false,
        attachments: []
      },
      {
        id: 6,
        name: '优化移动端适配',
        description: '优化团队任务管理系统在移动端的显示效果，确保在不同尺寸的设备上都能正常使用。',
        type: '开发',
        status: '未开始',
        priority: '低',
        assignee: 5,
        dueDate: '2023-07-10',
        createdAt: '2023-06-18T10:15:00.000Z',
        hasAttachments: false,
        attachments: []
      }
    ]
  }),
  
  getters: {
    getTaskById: (state) => (id) => {
      return state.tasks.find(task => task.id === id)
    },
    
    getTasksByStatus: (state) => (status) => {
      return state.tasks.filter(task => task.status === status)
    },
    
    getTasksByAssignee: (state) => (assigneeId) => {
      return state.tasks.filter(task => task.assignee === assigneeId)
    },
    
    getTasksByPriority: (state) => (priority) => {
      return state.tasks.filter(task => task.priority === priority)
    },
    
    getTasksByType: (state) => (type) => {
      return state.tasks.filter(task => task.type === type)
    }
  },
  
  actions: {
    // 获取任务列表（模拟API调用）
    async fetchTasks() {
      // 在实际应用中，这里应该是一个API调用
      // 这里使用setTimeout模拟异步操作
      return new Promise((resolve) => {
        setTimeout(() => {
          // 这里不做任何操作，因为我们已经在state中初始化了任务数据
          resolve(this.tasks)
        }, 500)
      })
    },
    
    // 添加新任务
    async addTask(taskData) {
      // 在实际应用中，这里应该是一个API调用
      return new Promise((resolve) => {
        setTimeout(() => {
          // 生成新的任务ID
          const newId = Math.max(...this.tasks.map(task => task.id), 0) + 1
          
          // 创建新任务对象
          const newTask = {
            id: newId,
            ...taskData,
            createdAt: new Date().toISOString()
          }
          
          // 添加到任务列表
          this.tasks.push(newTask)
          
          resolve(newTask)
        }, 300)
      })
    },
    
    // 更新任务
    async updateTask(taskData) {
      // 在实际应用中，这里应该是一个API调用
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const index = this.tasks.findIndex(task => task.id === taskData.id)
          
          if (index !== -1) {
            // 更新任务
            this.tasks[index] = {
              ...this.tasks[index],
              ...taskData
            }
            
            resolve(this.tasks[index])
          } else {
            reject(new Error('任务不存在'))
          }
        }, 300)
      })
    },
    
    // 更新任务状态
    async updateTaskStatus(taskId, newStatus) {
      // 在实际应用中，这里应该是一个API调用
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const index = this.tasks.findIndex(task => task.id === taskId)
          
          if (index !== -1) {
            // 更新任务状态
            this.tasks[index].status = newStatus
            
            // 如果有备注，可以添加到任务的历史记录中
            // 这里简化处理，实际应用中可能需要更复杂的逻辑
            
            resolve(this.tasks[index])
          } else {
            reject(new Error('任务不存在'))
          }
        }, 300)
      })
    },
    
    // 删除任务
    async deleteTask(taskId) {
      // 在实际应用中，这里应该是一个API调用
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const index = this.tasks.findIndex(task => task.id === taskId)
          
          if (index !== -1) {
            // 删除任务
            this.tasks.splice(index, 1)
            
            resolve(true)
          } else {
            reject(new Error('任务不存在'))
          }
        }, 300)
      })
    }
  }
})