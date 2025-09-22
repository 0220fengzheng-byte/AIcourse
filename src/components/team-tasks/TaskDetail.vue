<template>
  <div class="task-detail">
    <div class="task-header">
      <div class="task-meta">
        <div class="task-id">任务ID: {{ task.id }}</div>
        <div class="task-created">创建时间: {{ formatDate(task.createdAt) }}</div>
      </div>
      <div class="task-badges">
        <span class="tag" :class="'task-type-' + task.type">{{ task.type }}</span>
        <span class="status-badge" :class="'status-' + task.status">{{ task.status }}</span>
        <span class="priority-badge" :class="'priority-' + task.priority">{{ task.priority }}</span>
      </div>
    </div>
    
    <div v-if="!isEditing" class="task-content">
      <h2 class="task-name">{{ task.name }}</h2>
      <div class="task-description">
        <p>{{ task.description }}</p>
      </div>
      
      <div class="task-info-grid">
        <div class="task-info-item">
          <div class="info-label">负责人</div>
          <div class="info-value">
            <template v-if="task.customAssigneeName">
              <el-avatar :size="24">{{ getInitials(task.customAssigneeName) }}</el-avatar>
              <span>{{ task.customAssigneeName }} (自定义)</span>
            </template>
            <template v-else>
              <el-avatar :size="24" :src="getTeamMemberAvatar(task.assignee)">{{ getTeamMemberInitials(task.assignee) }}</el-avatar>
              <span>{{ getTeamMemberName(task.assignee) }}</span>
            </template>
          </div>
        </div>
        
        <div class="task-info-item">
          <div class="info-label">提需人</div>
          <div class="info-value">
            <template v-if="task.customRequesterName">
              <el-avatar :size="24">{{ getInitials(task.customRequesterName) }}</el-avatar>
              <span>{{ task.customRequesterName }} (自定义)</span>
            </template>
            <template v-else>
              <el-avatar :size="24" :src="getTeamMemberAvatar(task.requester)">{{ getTeamMemberInitials(task.requester) }}</el-avatar>
              <span>{{ getTeamMemberName(task.requester) }}</span>
            </template>
          </div>
        </div>
        
        <div class="task-info-item">
          <div class="info-label">截止日期</div>
          <div class="info-value" :class="{ 'overdue': isOverdue(task) }">
            {{ formatDate(task.dueDate) }}
            <span v-if="isOverdue(task)" class="overdue-tag">已逾期</span>
          </div>
        </div>
        
        <div v-if="task.documentLink" class="task-info-item">
          <div class="info-label">文档链接</div>
          <div class="info-value document-link">
            <a :href="task.documentLink" target="_blank" rel="noopener noreferrer">
              <i class="el-icon-link"></i>
              {{ getDocumentLinkText(task.documentLink) }}
            </a>
          </div>
        </div>
      </div>
      
      <div v-if="task.attachments && task.attachments.length > 0" class="task-attachments">
        <h3>附件</h3>
        <div class="attachment-list">
          <div v-for="(attachment, index) in task.attachments" :key="index" class="attachment-item">
            <div class="attachment-icon">
              <i class="el-icon-document" v-if="isDocument(attachment.type)"></i>
              <i class="el-icon-picture" v-else-if="isImage(attachment.type)"></i>
              <i class="el-icon-paperclip" v-else></i>
            </div>
            <div class="attachment-info">
              <div class="attachment-name">{{ attachment.name }}</div>
              <div class="attachment-size">{{ formatFileSize(attachment.size) }}</div>
            </div>
            <div class="attachment-actions">
              <button class="btn-icon" @click="downloadAttachment(attachment)">
                <i class="el-icon-download"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="task-actions">
        <el-button @click="startEditing">编辑任务</el-button>
        <el-button @click="$emit('close')">关闭</el-button>
      </div>
    </div>
    
    <div v-else class="task-edit-form">
      <TaskForm 
        :task="task" 
        :team-members="teamMembers"
        :type-options="['设计', '开发', '测试', '文档', '运营', '其他']"
        :priority-options="['高', '中', '低']"
        @submit="updateTask"
        @cancel="cancelEditing"
      />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import TaskForm from './TaskForm.vue'

export default {
  name: 'TaskDetail',
  components: {
    TaskForm
  },
  props: {
    task: {
      type: Object,
      required: true
    },
    teamMembers: {
      type: Array,
      required: true
    }
  },
  emits: ['update-task', 'close'],
  setup(props, { emit }) {
    const isEditing = ref(false)
    
    const startEditing = () => {
      isEditing.value = true
    }
    
    const cancelEditing = () => {
      isEditing.value = false
    }
    
    const updateTask = (taskData) => {
      emit('update-task', taskData)
    }
    
    const getTeamMemberName = (userId) => {
      const member = props.teamMembers.find(m => m.id === userId)
      return member ? member.name : '未分配'
    }
    
    const getTeamMemberAvatar = (userId) => {
      const member = props.teamMembers.find(m => m.id === userId)
      return member && member.avatar ? member.avatar : ''
    }
    
    const getTeamMemberInitials = (userId) => {
      const member = props.teamMembers.find(m => m.id === userId)
      return member ? member.name.charAt(0) : '?'
    }
    
    // 获取自定义姓名的首字母
    const getInitials = (name) => {
      if (!name) return '?'
      return name.charAt(0).toUpperCase()
    }
    
    // 获取文档链接的显示文本
    const getDocumentLinkText = (url) => {
      if (!url) return ''
      
      try {
        // 尝试解析URL
        const urlObj = new URL(url)
        
        // 根据域名判断文档类型
        if (urlObj.hostname.includes('feishu.cn') || urlObj.hostname.includes('feishu.com')) {
          return '飞书文档'
        } else if (urlObj.hostname.includes('docs.google.com')) {
          return '谷歌文档'
        } else if (urlObj.hostname.includes('yuque.com')) {
          return '语雀文档'
        } else if (urlObj.hostname.includes('shimo.im')) {
          return '石墨文档'
        } else {
          // 如果无法识别，则显示域名
          return urlObj.hostname
        }
      } catch (e) {
        // 如果URL解析失败，则显示原始URL
        return url.length > 30 ? url.substring(0, 30) + '...' : url
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '无日期'
      
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const isOverdue = (task) => {
      if (!task.dueDate) return false
      
      const dueDate = new Date(task.dueDate)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      return dueDate < today && task.status !== '已完成'
    }
    
    const isDocument = (type) => {
      const docTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
      return docTypes.includes(type)
    }
    
    const isImage = (type) => {
      return type && type.startsWith('image/')
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const downloadAttachment = (attachment) => {
      // 在实际应用中，这里应该实现真正的文件下载逻辑
      // 这里只是一个模拟示例
      if (attachment.url) {
        const link = document.createElement('a')
        link.href = attachment.url
        link.download = attachment.name
        link.click()
      }
    }
    
    return {
      isEditing,
      startEditing,
      cancelEditing,
      updateTask,
      getTeamMemberName,
      getTeamMemberAvatar,
      getTeamMemberInitials,
      getInitials,
      getDocumentLinkText,
      formatDate,
      isOverdue,
      isDocument,
      isImage,
      formatFileSize,
      downloadAttachment
    }
  }
}
</script>

<style lang="scss" scoped>
.task-detail {
  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    
    .task-meta {
      .task-id {
        font-family: monospace;
        color: var(--text-medium);
        margin-bottom: 0.25rem;
      }
      
      .task-created {
        color: var(--text-medium);
        font-size: 0.9rem;
      }
    }
    
    .task-badges {
      display: flex;
      gap: 0.5rem;
    }
  }
  
  .task-content {
    .task-name {
      font-size: 1.5rem;
      margin-bottom: 1rem;
      color: var(--text-dark);
    }
    
    .task-description {
      margin-bottom: 1.5rem;
      color: var(--text-dark);
      line-height: 1.6;
      
      p {
        margin: 0;
        white-space: pre-line;
      }
    }
    
    .task-info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
      
      .task-info-item {
        .info-label {
          font-weight: bold;
          margin-bottom: 0.5rem;
          color: var(--text-medium);
        }
        
        .info-value {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          
          &.overdue {
            color: var(--danger);
            
            .overdue-tag {
              display: inline-block;
              padding: 0.1rem 0.5rem;
              background-color: var(--danger);
              color: white;
              border-radius: 4px;
              font-size: 0.75rem;
            }
          }
          
          &.document-link {
            a {
              display: flex;
              align-items: center;
              gap: 0.5rem;
              color: var(--primary-blue);
              text-decoration: none;
              
              &:hover {
                text-decoration: underline;
              }
              
              i {
                font-size: 1rem;
              }
            }
          }
        }
      }
    }
    
    .task-attachments {
      margin-bottom: 1.5rem;
      
      h3 {
        margin-bottom: 1rem;
        color: var(--text-dark);
      }
      
      .attachment-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        
        .attachment-item {
          display: flex;
          align-items: center;
          padding: 0.75rem;
          background-color: var(--bg-light);
          border-radius: 8px;
          
          .attachment-icon {
            font-size: 1.5rem;
            margin-right: 1rem;
            color: var(--primary-blue);
          }
          
          .attachment-info {
            flex-grow: 1;
            
            .attachment-name {
              font-weight: bold;
              margin-bottom: 0.25rem;
              color: var(--text-dark);
            }
            
            .attachment-size {
              font-size: 0.85rem;
              color: var(--text-medium);
            }
          }
          
          .attachment-actions {
            .btn-icon {
              background: none;
              border: none;
              cursor: pointer;
              color: var(--text-medium);
              font-size: 1.2rem;
              
              &:hover {
                color: var(--primary-blue);
              }
            }
          }
        }
      }
    }
    
    .task-actions {
      display: flex;
      justify-content: flex-end;
      gap: 1rem;
      margin-top: 1rem;
    }
  }
}
</style>