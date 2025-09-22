import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [
      {
        id: 1,
        title: '任务状态变更',
        content: '任务 "设计团队任务管理系统UI" 状态从 "进行中" 变更为 "已完成"',
        type: 'info',
        time: '2023-06-15T10:30:00.000Z',
        read: true
      },
      {
        id: 2,
        title: '新任务创建',
        content: '任务 "实现任务列表组件" 已创建',
        type: 'info',
        time: '2023-06-05T09:30:00.000Z',
        read: true
      },
      {
        id: 3,
        title: '任务截止日期提醒',
        content: '任务 "实现任务列表组件" 将在3天后截止',
        type: 'warning',
        time: '2023-06-17T08:00:00.000Z',
        read: false
      }
    ]
  }),
  
  getters: {
    unreadNotifications: (state) => {
      return state.notifications.filter(notification => !notification.read)
    },
    
    getNotificationById: (state) => (id) => {
      return state.notifications.find(notification => notification.id === id)
    }
  },
  
  actions: {
    // 添加新通知
    addNotification(notification) {
      // 生成新的通知ID
      const newId = Math.max(...this.notifications.map(n => n.id), 0) + 1
      
      // 创建新通知对象
      const newNotification = {
        id: newId,
        ...notification,
        read: false,
        time: notification.time || new Date().toISOString()
      }
      
      // 添加到通知列表
      this.notifications.push(newNotification)
      
      return newNotification
    },
    
    // 标记通知为已读
    markAsRead(notificationId) {
      const notification = this.notifications.find(n => n.id === notificationId)
      
      if (notification) {
        notification.read = true
      }
    },
    
    // 标记所有通知为已读
    markAllAsRead() {
      this.notifications.forEach(notification => {
        notification.read = true
      })
    },
    
    // 删除通知
    deleteNotification(notificationId) {
      const index = this.notifications.findIndex(n => n.id === notificationId)
      
      if (index !== -1) {
        this.notifications.splice(index, 1)
      }
    },
    
    // 清空所有通知
    clearAllNotifications() {
      this.notifications = []
    }
  }
})