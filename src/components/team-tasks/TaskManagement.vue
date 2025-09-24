<template>
  <div class="task-management">
    <!-- 页面头部 -->
    <div class="task-header rainbow-card">
      <div class="task-header-left">
        <h2>团队任务列表</h2>
        <p>共 {{ totalTasks }} 个任务，{{ completedTasksCount }} 个已完成</p>
      </div>
      <div class="task-header-right">
        <button class="btn btn-primary" @click="showNewTaskModal = true">
          <i class="el-icon-plus"></i> 新建任务
        </button>
        <button class="btn btn-info" @click="showNotificationCenter = true">
          <i class="el-icon-bell"></i>
          <span v-if="unreadNotifications > 0" class="notification-badge">{{ unreadNotifications }}</span>
        </button>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar rainbow-card">
      <div class="filter-group">
        <label>任务状态</label>
        <el-select v-model="filters.status" placeholder="全部状态" clearable>
          <el-option v-for="status in statusOptions" :key="status" :label="status" :value="status" />
        </el-select>
      </div>
      
      <div class="filter-group">
        <label>任务类型</label>
        <el-select v-model="filters.type" placeholder="全部类型" clearable>
          <el-option v-for="type in typeOptions" :key="type" :label="type" :value="type" />
        </el-select>
      </div>
      
      <div class="filter-group">
        <label>优先级</label>
        <el-select v-model="filters.priority" placeholder="全部优先级" clearable>
          <el-option v-for="priority in priorityOptions" :key="priority" :label="priority" :value="priority" />
        </el-select>
      </div>
      
      <div class="filter-group">
        <label>负责人</label>
        <el-select v-model="filters.assignee" placeholder="全部负责人" clearable>
          <el-option v-for="user in teamMembers" :key="user.id" :label="user.name" :value="user.id" />
        </el-select>
      </div>
      
      <div class="filter-group search-group">
        <label>搜索</label>
        <el-input v-model="filters.search" placeholder="搜索任务名称或描述" clearable>
          <template #suffix>
            <i class="el-icon-search"></i>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="task-list rainbow-card" v-loading="loading">
      <div v-if="filteredTasks.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>暂无任务</h3>
        <p>当前筛选条件下没有找到任务，请尝试调整筛选条件或创建新任务</p>
        <button class="btn btn-primary" @click="showNewTaskModal = true">
          <i class="el-icon-plus"></i> 新建任务
        </button>
      </div>
      
      <table v-else class="task-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>任务名称</th>
            <th>类型</th>
            <th>状态</th>
            <th>优先级</th>
            <th>负责人</th>
            <th>文档链接</th>
            <th>附件</th>
            <th>截止日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in paginatedTasks" :key="task.id" class="task-row">
            <td class="task-id">{{ task.id }}</td>
            <td class="task-name" @click="openTaskDetail(task)">
              {{ task.name }}
              <div class="task-icons">
                <span v-if="task.hasAttachments" class="icon attachment-icon" title="有附件">
                  <i class="el-icon-paperclip"></i>
                </span>
                <span v-if="task.documentLink" class="icon document-link-icon" title="有文档链接">
                  <i class="el-icon-link"></i>
                </span>
              </div>
            </td>
            <td>
              <span class="tag" :class="'task-type-' + task.type">{{ task.type }}</span>
            </td>
            <td>
              <span class="status-badge" :class="'status-' + task.status">{{ task.status }}</span>
            </td>
            <td>
              <span class="priority-badge" :class="'priority-' + task.priority">{{ task.priority }}</span>
            </td>
            <td class="task-assignee">
              <template v-if="task.customAssigneeName">
                <el-avatar :size="24">{{ getInitials(task.customAssigneeName) }}</el-avatar>
                <span>{{ task.customAssigneeName }}</span>
              </template>
              <template v-else>
                <el-avatar :size="24" :src="getTeamMemberAvatar(task.assignee)">{{ getTeamMemberInitials(task.assignee) }}</el-avatar>
                <span>{{ getTeamMemberName(task.assignee) }}</span>
              </template>
            </td>
            <td class="task-doc-link">
              <div v-if="task.documentLink" class="document-link-cell">
                <a :href="task.documentLink" target="_blank" rel="noopener noreferrer" @click.stop>
                  <i class="el-icon-link"></i>
                  {{ getDocumentLinkText(task.documentLink) }}
                </a>
              </div>
              <div v-else class="no-document">-</div>
            </td>
            <td class="task-attachments">
              <div v-if="task.hasAttachments && task.attachments && task.attachments.length > 0" class="attachments-cell">
                <div v-for="(attachment, index) in task.attachments.slice(0, 2)" :key="index" class="attachment-item">
                  <i :class="getAttachmentIcon(attachment.type)" class="attachment-icon-small"></i>
                  <span class="attachment-name" :title="attachment.name">{{ truncateFileName(attachment.name) }}</span>
                </div>
                <div v-if="task.attachments.length > 2" class="more-attachments">
                  +{{ task.attachments.length - 2 }} 更多
                </div>
              </div>
              <div v-else class="no-attachments">-</div>
            </td>
            <td :class="{ 'overdue': isOverdue(task) }">
              {{ formatDate(task.dueDate) }}
              <span v-if="isOverdue(task)" class="overdue-tag">已逾期</span>
            </td>
            <td class="task-actions">
              <el-dropdown trigger="click">
                <button class="btn-icon"><i class="el-icon-more"></i></button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="openTaskDetail(task)">
                      <i class="el-icon-view"></i> 查看详情
                    </el-dropdown-item>
                    <el-dropdown-item @click="openChangeStatus(task)">
                      <i class="el-icon-refresh"></i> 修改状态
                    </el-dropdown-item>
                    <el-dropdown-item @click="editTask(task)">
                      <i class="el-icon-edit"></i> 编辑任务
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="deleteTask(task)">
                      <i class="el-icon-delete"></i> 删除任务
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页控制 -->
    <div class="pagination-control" v-if="filteredTasks.length > 0">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredTasks.length"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 新建任务弹窗 -->
    <el-dialog
      v-model="showNewTaskModal"
      title="新建任务"
      width="600px"
      :before-close="closeNewTaskModal"
    >
      <TaskForm 
        :team-members="teamMembers" 
        :type-options="typeOptions"
        :priority-options="priorityOptions"
        @submit="createTask"
        @cancel="closeNewTaskModal"
      />
    </el-dialog>

    <!-- 任务详情弹窗 -->
    <el-dialog
      v-model="showTaskDetailModal"
      title="任务详情"
      width="700px"
      :before-close="closeTaskDetailModal"
    >
      <TaskDetail 
        v-if="currentTask" 
        :task="currentTask" 
        :team-members="teamMembers"
        @update-task="updateTask"
        @close="closeTaskDetailModal"
      />
    </el-dialog>

    <!-- 修改状态弹窗 -->
    <el-dialog
      v-model="showChangeStatusModal"
      title="修改任务状态"
      width="400px"
      :before-close="closeChangeStatusModal"
    >
      <StatusChange 
        v-if="currentTask" 
        :task="currentTask" 
        :status-options="statusOptions"
        @update-status="updateTaskStatus"
        @cancel="closeChangeStatusModal"
      />
    </el-dialog>

    <!-- 通知中心弹窗 -->
    <el-drawer
      v-model="showNotificationCenter"
      title="通知中心"
      direction="rtl"
      size="350px"
    >
      <NotificationCenter 
        :notifications="notifications" 
        @mark-as-read="markNotificationAsRead"
        @mark-all-as-read="markAllNotificationsAsRead"
      />
    </el-drawer>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import TaskForm from './TaskForm.vue'
import TaskDetail from './TaskDetail.vue'
import StatusChange from './StatusChange.vue'
import NotificationCenter from './NotificationCenter.vue'
import { useTaskStore } from '@/stores/taskStore'
import { useNotificationStore } from '@/stores/notificationStore'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'TaskManagement',
  components: {
    TaskForm,
    TaskDetail,
    StatusChange,
    NotificationCenter
  },
  setup() {
    const taskStore = useTaskStore()
    const notificationStore = useNotificationStore()
    
    // 状态变量
    const loading = ref(false)
    const showNewTaskModal = ref(false)
    const showTaskDetailModal = ref(false)
    const showChangeStatusModal = ref(false)
    const showNotificationCenter = ref(false)
    const currentTask = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    // 筛选条件
    const filters = reactive({
      status: '',
      type: '',
      priority: '',
      assignee: '',
      search: ''
    })
    
    // 选项数据
    const statusOptions = ['未开始', '进行中', '已完成', '已取消']
    const typeOptions = ['设计', '开发', '测试', '文档', '运营', '其他']
    const priorityOptions = ['高', '中', '低']
    
    // 团队成员数据
    const teamMembers = [
      { id: 1, name: '张三', avatar: '' },
      { id: 2, name: '李四', avatar: '' },
      { id: 3, name: '王五', avatar: '' },
      { id: 4, name: '赵六', avatar: '' },
      { id: 5, name: '钱七', avatar: '' }
    ]
    
    // 计算属性
    const filteredTasks = computed(() => {
      return taskStore.tasks.filter(task => {
        // 状态筛选
        if (filters.status && task.status !== filters.status) return false
        
        // 类型筛选
        if (filters.type && task.type !== filters.type) return false
        
        // 优先级筛选
        if (filters.priority && task.priority !== filters.priority) return false
        
        // 负责人筛选
        if (filters.assignee && task.assignee !== parseInt(filters.assignee)) return false
        
        // 搜索筛选
        if (filters.search) {
          const searchLower = filters.search.toLowerCase()
          return (
            task.name.toLowerCase().includes(searchLower) ||
            task.description.toLowerCase().includes(searchLower)
          )
        }
        
        return true
      })
    })
    
    const paginatedTasks = computed(() => {
      const startIndex = (currentPage.value - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      return filteredTasks.value.slice(startIndex, endIndex)
    })
    
    const totalTasks = computed(() => taskStore.tasks.length)
    
    const completedTasksCount = computed(() => {
      return taskStore.tasks.filter(task => task.status === '已完成').length
    })
    
    const notifications = computed(() => notificationStore.notifications)
    
    const unreadNotifications = computed(() => {
      return notificationStore.notifications.filter(notification => !notification.read).length
    })
    
    // 方法
    const loadTasks = async () => {
      loading.value = true
      try {
        await taskStore.fetchTasks()
      } catch (error) {
        ElMessage.error('加载任务失败：' + error.message)
      } finally {
        loading.value = false
      }
    }
    
    const handlePageChange = (page) => {
      currentPage.value = page
    }
    
    const openTaskDetail = (task) => {
      currentTask.value = task
      showTaskDetailModal.value = true
    }
    
    const closeTaskDetailModal = () => {
      showTaskDetailModal.value = false
      currentTask.value = null
    }
    
    const openChangeStatus = (task) => {
      currentTask.value = task
      showChangeStatusModal.value = true
    }
    
    const closeChangeStatusModal = () => {
      showChangeStatusModal.value = false
      currentTask.value = null
    }
    
    const closeNewTaskModal = () => {
      showNewTaskModal.value = false
    }
    
    const createTask = async (taskData) => {
      try {
        await taskStore.addTask(taskData)
        ElMessage.success('任务创建成功')
        showNewTaskModal.value = false
        
        // 添加通知
        notificationStore.addNotification({
          title: '新任务创建',
          content: `任务 "${taskData.name}" 已创建`,
          type: 'info',
          time: new Date().toISOString()
        })
      } catch (error) {
        ElMessage.error('创建任务失败：' + error.message)
      }
    }
    
    const updateTask = async (taskData) => {
      try {
        await taskStore.updateTask(taskData)
        ElMessage.success('任务更新成功')
        showTaskDetailModal.value = false
        currentTask.value = null
        
        // 添加通知
        notificationStore.addNotification({
          title: '任务已更新',
          content: `任务 "${taskData.name}" 已更新`,
          type: 'info',
          time: new Date().toISOString()
        })
      } catch (error) {
        ElMessage.error('更新任务失败：' + error.message)
      }
    }
    
    const updateTaskStatus = async (taskId, newStatus) => {
      try {
        const task = taskStore.getTaskById(taskId)
        if (!task) throw new Error('任务不存在')
        
        const oldStatus = task.status
        await taskStore.updateTaskStatus(taskId, newStatus)
        
        ElMessage.success(`任务状态已从 "${oldStatus}" 更新为 "${newStatus}"`)
        showChangeStatusModal.value = false
        currentTask.value = null
        
        // 添加通知
        notificationStore.addNotification({
          title: '任务状态变更',
          content: `任务 "${task.name}" 状态从 "${oldStatus}" 变更为 "${newStatus}"`,
          type: 'info',
          time: new Date().toISOString()
        })
      } catch (error) {
        ElMessage.error('更新任务状态失败：' + error.message)
      }
    }
    
    const editTask = (task) => {
      currentTask.value = task
      showTaskDetailModal.value = true
    }
    
    const deleteTask = (task) => {
      ElMessageBox.confirm(
        `确定要删除任务 "${task.name}" 吗？此操作不可撤销。`,
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await taskStore.deleteTask(task.id)
          ElMessage.success('任务删除成功')
          
          // 添加通知
          notificationStore.addNotification({
            title: '任务已删除',
            content: `任务 "${task.name}" 已被删除`,
            type: 'warning',
            time: new Date().toISOString()
          })
        } catch (error) {
          ElMessage.error('删除任务失败：' + error.message)
        }
      }).catch(() => {
        // 用户取消删除
      })
    }
    
    const markNotificationAsRead = (notificationId) => {
      notificationStore.markAsRead(notificationId)
    }
    
    const markAllNotificationsAsRead = () => {
      notificationStore.markAllAsRead()
    }
    
    const getTeamMemberName = (userId) => {
      const member = teamMembers.find(m => m.id === userId)
      return member ? member.name : '未分配'
    }
    
    const getTeamMemberAvatar = (userId) => {
      const member = teamMembers.find(m => m.id === userId)
      return member && member.avatar ? member.avatar : ''
    }
    
    const getTeamMemberInitials = (userId) => {
      const member = teamMembers.find(m => m.id === userId)
      return member ? member.name.charAt(0) : '?'
    }
    
    const getInitials = (name) => {
      if (!name) return '?'
      return name.charAt(0).toUpperCase()
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '无截止日期'
      
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }
    
    const isOverdue = (task) => {
      if (!task.dueDate) return false

      const dueDate = new Date(task.dueDate)
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      return dueDate < today && task.status !== '已完成'
    }

    const getDocumentLinkText = (url) => {
      if (!url) return ''

      try {
        const urlObj = new URL(url)

        if (urlObj.hostname.includes('feishu.cn') || urlObj.hostname.includes('feishu.com')) {
          return '飞书文档'
        } else if (urlObj.hostname.includes('docs.google.com')) {
          return '谷歌文档'
        } else if (urlObj.hostname.includes('yuque.com')) {
          return '语雀文档'
        } else if (urlObj.hostname.includes('shimo.im')) {
          return '石墨文档'
        } else {
          return urlObj.hostname
        }
      } catch (e) {
        return url.length > 20 ? url.substring(0, 20) + '...' : url
      }
    }

    const getAttachmentIcon = (type) => {
      if (!type) return 'el-icon-paperclip'

      if (type.startsWith('image/')) {
        return 'el-icon-picture'
      } else if (type.includes('pdf')) {
        return 'el-icon-document'
      } else if (type.includes('word') || type.includes('document')) {
        return 'el-icon-document'
      } else if (type.includes('excel') || type.includes('spreadsheet')) {
        return 'el-icon-s-data'
      } else if (type.includes('powerpoint') || type.includes('presentation')) {
        return 'el-icon-data-analysis'
      } else {
        return 'el-icon-paperclip'
      }
    }

    const truncateFileName = (name, maxLength = 15) => {
      if (!name) return ''
      return name.length > maxLength ? name.substring(0, maxLength) + '...' : name
    }
    
    // 生命周期钩子
    onMounted(() => {
      loadTasks()
    })
    
    return {
      loading,
      showNewTaskModal,
      showTaskDetailModal,
      showChangeStatusModal,
      showNotificationCenter,
      currentTask,
      currentPage,
      pageSize,
      filters,
      statusOptions,
      typeOptions,
      priorityOptions,
      teamMembers,
      filteredTasks,
      paginatedTasks,
      totalTasks,
      completedTasksCount,
      notifications,
      unreadNotifications,
      handlePageChange,
      openTaskDetail,
      closeTaskDetailModal,
      openChangeStatus,
      closeChangeStatusModal,
      closeNewTaskModal,
      createTask,
      updateTask,
      updateTaskStatus,
      editTask,
      deleteTask,
      markNotificationAsRead,
      markAllNotificationsAsRead,
      getTeamMemberName,
      getTeamMemberAvatar,
      getTeamMemberInitials,
      getInitials,
      formatDate,
      isOverdue,
      getDocumentLinkText,
      getAttachmentIcon,
      truncateFileName
    }
  }
}
</script>

<style lang="scss" scoped>
.task-management {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  
  .task-header-left {
    h2 {
      margin: 0 0 0.5rem 0;
      color: var(--text-dark);
    }
    
    p {
      margin: 0;
      color: var(--text-medium);
    }
  }
  
  .task-header-right {
    display: flex;
    gap: 1rem;
    
    .btn-info {
      position: relative;
      
      .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background-color: var(--danger);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
      }
    }
  }
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1.5rem;
  
  .filter-group {
    display: flex;
    flex-direction: column;
    min-width: 150px;
    
    label {
      margin-bottom: 0.5rem;
      font-weight: bold;
      color: var(--text-dark);
    }
  }
  
  .search-group {
    flex-grow: 1;
  }
}

.task-list {
  padding: 1.5rem;
  
  .task-table {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
    table-layout: fixed;
    
    th, td {
      padding: 0.75rem;
      text-align: left;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      box-sizing: border-box;
    }
    
    thead tr {
      border-bottom: 2px solid #e0e0e0;
    }
    
    th {
      font-weight: bold;
      color: var(--text-dark);
      background-color: var(--bg-light);
    }
    
    th:nth-child(1) { width: 60px; } /* ID列 */
    th:nth-child(2) { width: 18%; } /* 任务名称列 */
    th:nth-child(3) { width: 100px; } /* 类型列 */
    th:nth-child(4) { width: 100px; } /* 状态列 */
    th:nth-child(5) { width: 100px; } /* 优先级列 */
    th:nth-child(6) { width: 140px; } /* 负责人列 */
    th:nth-child(7) { width: 150px; } /* 文档链接列 */
    th:nth-child(8) { width: 150px; } /* 附件列 */
    th:nth-child(9) { width: 120px; } /* 截止日期列 */
    th:nth-child(10) { width: 60px; } /* 操作列 */
    
    tbody tr {
      border-bottom: 1px solid #e0e0e0;
    }
    
    .task-row {
      &:hover {
        background-color: var(--bg-light);
      }
    }
    
    .task-id {
      color: var(--text-medium);
      font-family: monospace;
      width: 60px;
    }
    
    .task-name {
        font-weight: bold;
        cursor: pointer;
        color: var(--primary-blue);
        display: flex;
        align-items: center;
        
        &:hover {
          text-decoration: underline;
        }
        
        .task-icons {
          display: flex;
          align-items: center;
          gap: 5px;
          margin-left: 8px;
          flex-shrink: 0;
          
          .icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-medium);
            font-size: 14px;
          }
          
          .attachment-icon {
            color: #67c23a;
          }
          
          .document-link-icon {
            color: #409eff;
          }
        }
      }
    
    .task-assignee {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      
      span {
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
    
    .task-actions {
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

    .task-doc-link {
      .document-link-cell {
        a {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: var(--primary-blue);
          text-decoration: none;
          font-size: 0.9rem;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          transition: background-color 0.2s;

          &:hover {
            text-decoration: underline;
            background-color: rgba(64, 158, 255, 0.1);
          }

          i {
            font-size: 1rem;
          }
        }
      }

      .no-document {
        color: var(--text-medium);
        text-align: center;
        font-size: 0.9rem;
      }
    }

    .task-attachments {
      .attachments-cell {
        .attachment-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.25rem;
          font-size: 0.85rem;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          background-color: rgba(103, 194, 58, 0.1);
          transition: background-color 0.2s;

          &:hover {
            background-color: rgba(103, 194, 58, 0.2);
          }

          .attachment-icon-small {
            font-size: 1rem;
            color: var(--primary-green);
            flex-shrink: 0;
          }

          .attachment-name {
            color: var(--text-dark);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 100px;
          }
        }

        .more-attachments {
          font-size: 0.8rem;
          color: var(--text-medium);
          margin-top: 0.25rem;
          padding: 0.25rem 0.5rem;
          background-color: rgba(103, 194, 58, 0.05);
          border-radius: 4px;
          text-align: center;
        }
      }

      .no-attachments {
        color: var(--text-medium);
        text-align: center;
        font-size: 0.9rem;
      }
    }

    .overdue {
      color: var(--danger);

      .overdue-tag {
        display: inline-block;
        margin-left: 0.5rem;
        padding: 0.1rem 0.5rem;
        background-color: var(--danger);
        color: white;
        border-radius: 4px;
        font-size: 0.75rem;
      }
    }
  }
}

.pagination-control {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

/* 任务类型标签样式 */
.task-type-设计 {
  background-color: rgba(253, 121, 168, 0.2);
  color: var(--task-design);
}

.task-type-开发 {
  background-color: rgba(116, 185, 255, 0.2);
  color: var(--task-development);
}

.task-type-测试 {
  background-color: rgba(85, 239, 196, 0.2);
  color: var(--task-testing);
}

.task-type-文档 {
  background-color: rgba(162, 155, 254, 0.2);
  color: var(--task-planning);
}

.task-type-运营 {
  background-color: rgba(225, 112, 85, 0.2);
  color: var(--task-operation);
}

.task-type-其他 {
  background-color: rgba(178, 190, 195, 0.2);
  color: var(--text-medium);
}

/* 彩虹卡片效果 */
.rainbow-card {
  background-color: var(--bg-white);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(
      to right,
      var(--primary-pink),
      var(--primary-blue),
      var(--primary-green),
      var(--primary-yellow)
    );
  }
}
</style>