<template>
  <div class="status-change">
    <div class="current-status">
      <div class="status-label">当前状态</div>
      <div class="status-value">
        <span class="status-badge" :class="'status-' + task.status">{{ task.status }}</span>
      </div>
    </div>
    
    <div class="new-status">
      <div class="status-label">新状态</div>
      <el-radio-group v-model="selectedStatus">
        <el-radio 
          v-for="status in availableStatuses" 
          :key="status" 
          :label="status"
          :disabled="status === task.status"
        >
          <span class="status-badge" :class="'status-' + status">{{ status }}</span>
        </el-radio>
      </el-radio-group>
    </div>
    
    <div class="status-comment">
      <div class="status-label">状态变更备注 (可选)</div>
      <el-input 
        v-model="comment" 
        type="textarea" 
        :rows="3" 
        placeholder="请输入状态变更的原因或备注信息" 
      />
    </div>
    
    <div class="status-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button 
        type="primary" 
        @click="updateStatus" 
        :disabled="!selectedStatus || selectedStatus === task.status"
      >
        确认修改
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'StatusChange',
  props: {
    task: {
      type: Object,
      required: true
    },
    statusOptions: {
      type: Array,
      required: true
    }
  },
  emits: ['update-status', 'cancel'],
  setup(props, { emit }) {
    const selectedStatus = ref('')
    const comment = ref('')
    
    // 根据当前状态计算可用的下一个状态
    const availableStatuses = computed(() => {
      // 这里可以根据业务逻辑定义状态流转规则
      // 例如：未开始 -> 进行中 -> 已完成
      // 但这里简单返回所有状态选项
      return props.statusOptions
    })
    
    const updateStatus = () => {
      if (selectedStatus.value && selectedStatus.value !== props.task.status) {
        emit('update-status', props.task.id, selectedStatus.value, comment.value)
      }
    }
    
    return {
      selectedStatus,
      comment,
      availableStatuses,
      updateStatus
    }
  }
}
</script>

<style lang="scss" scoped>
.status-change {
  padding: 1rem;
  
  .current-status,
  .new-status,
  .status-comment {
    margin-bottom: 1.5rem;
  }
  
  .status-label {
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: var(--text-dark);
  }
  
  .el-radio {
    margin-right: 1.5rem;
    margin-bottom: 0.75rem;
  }
  
  .status-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
}
</style>