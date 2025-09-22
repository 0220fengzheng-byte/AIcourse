<template>
  <div class="notification-center">
    <div class="notification-header">
      <h3>通知中心</h3>
      <button 
        class="btn-text" 
        @click="$emit('mark-all-as-read')"
        :disabled="unreadCount === 0"
      >
        全部标为已读
      </button>
    </div>
    
    <div v-if="notifications.length === 0" class="empty-state">
      <div class="empty-icon">🔔</div>
      <h3>暂无通知</h3>
      <p>当有新的任务更新或系统消息时，将在这里显示</p>
    </div>
    
    <div v-else class="notification-list">
      <div 
        v-for="notification in sortedNotifications" 
        :key="notification.id" 
        class="notification-item"
        :class="{ 'unread': !notification.read }"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-icon" :class="'notification-type-' + notification.type">
          <i class="el-icon-info" v-if="notification.type === 'info'"></i>
          <i class="el-icon-success" v-else-if="notification.type === 'success'"></i>
          <i class="el-icon-warning" v-else-if="notification.type === 'warning'"></i>
          <i class="el-icon-error" v-else-if="notification.type === 'error'"></i>
        </div>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.content }}</div>
          <div class="notification-time">{{ formatTime(notification.time) }}</div>
        </div>
        <div class="notification-actions">
          <button class="btn-icon" @click.stop="markAsRead(notification.id)" v-if="!notification.read">
            <i class="el-icon-check"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'NotificationCenter',
  props: {
    notifications: {
      type: Array,
      required: true
    }
  },
  emits: ['mark-as-read', 'mark-all-as-read'],
  setup(props, { emit }) {
    // 按时间排序的通知列表，最新的在前面
    const sortedNotifications = computed(() => {
      return [...props.notifications].sort((a, b) => {
        return new Date(b.time) - new Date(a.time)
      })
    })
    
    // 未读通知数量
    const unreadCount = computed(() => {
      return props.notifications.filter(notification => !notification.read).length
    })
    
    // 标记通知为已读
    const markAsRead = (notificationId) => {
      emit('mark-as-read', notificationId)
    }
    
    // 格式化时间
    const formatTime = (timeString) => {
      const now = new Date()
      const notificationTime = new Date(timeString)
      const diffMs = now - notificationTime
      const diffMins = Math.floor(diffMs / (1000 * 60))
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
      
      if (diffMins < 1) {
        return '刚刚'
      } else if (diffMins < 60) {
        return `${diffMins}分钟前`
      } else if (diffHours < 24) {
        return `${diffHours}小时前`
      } else if (diffDays < 7) {
        return `${diffDays}天前`
      } else {
        return notificationTime.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        })
      }
    }
    
    return {
      sortedNotifications,
      unreadCount,
      markAsRead,
      formatTime
    }
  }
}
</script>

<style lang="scss" scoped>
.notification-center {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .notification-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--text-light);
    
    h3 {
      margin: 0;
      color: var(--text-dark);
    }
    
    .btn-text {
      background: none;
      border: none;
      color: var(--primary-blue);
      cursor: pointer;
      font-size: 0.9rem;
      
      &:hover {
        text-decoration: underline;
      }
      
      &:disabled {
        color: var(--text-light);
        cursor: default;
        text-decoration: none;
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
    text-align: center;
    
    .empty-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      color: var(--text-light);
    }
    
    h3 {
      color: var(--text-dark);
      margin-bottom: 0.5rem;
    }
    
    p {
      color: var(--text-medium);
    }
  }
  
  .notification-list {
    flex-grow: 1;
    overflow-y: auto;
    
    .notification-item {
      display: flex;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--text-light);
      cursor: pointer;
      transition: background-color 0.2s ease;
      
      &:hover {
        background-color: var(--bg-light);
      }
      
      &.unread {
        background-color: rgba(116, 185, 255, 0.1);
        
        &:hover {
          background-color: rgba(116, 185, 255, 0.15);
        }
        
        .notification-title {
          font-weight: bold;
        }
      }
      
      .notification-icon {
        margin-right: 1rem;
        font-size: 1.2rem;
        
        &.notification-type-info {
          color: var(--info);
        }
        
        &.notification-type-success {
          color: var(--success);
        }
        
        &.notification-type-warning {
          color: var(--warning);
        }
        
        &.notification-type-error {
          color: var(--danger);
        }
      }
      
      .notification-content {
        flex-grow: 1;
        
        .notification-title {
          margin-bottom: 0.25rem;
          color: var(--text-dark);
        }
        
        .notification-message {
          margin-bottom: 0.5rem;
          color: var(--text-medium);
        }
        
        .notification-time {
          font-size: 0.85rem;
          color: var(--text-light);
        }
      }
      
      .notification-actions {
        display: flex;
        align-items: center;
        
        .btn-icon {
          background: none;
          border: none;
          cursor: pointer;
          color: var(--text-medium);
          font-size: 1.2rem;
          
          &:hover {
            color: var(--success);
          }
        }
      }
    }
  }
}
</style>