<template>
  <div class="task-form">
    <el-form :model="taskForm" :rules="rules" ref="formRef" label-position="top">
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
      </el-form-item>
      
      <el-form-item label="任务描述" prop="description">
        <el-input 
          v-model="taskForm.description" 
          type="textarea" 
          :rows="4" 
          placeholder="请输入任务描述" 
        />
      </el-form-item>
      
      <div class="form-row">
        <el-form-item label="任务类型" prop="type" class="form-col">
          <el-select v-model="taskForm.type" placeholder="请选择任务类型">
            <el-option 
              v-for="type in typeOptions" 
              :key="type" 
              :label="type" 
              :value="type" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority" class="form-col">
          <el-select v-model="taskForm.priority" placeholder="请选择优先级">
            <el-option 
              v-for="priority in priorityOptions" 
              :key="priority" 
              :label="priority" 
              :value="priority" 
            />
          </el-select>
        </el-form-item>
      </div>
      
      <div class="form-row">
        <el-form-item label="负责人" prop="assignee" class="form-col">
          <div class="assignee-input">
            <el-select 
              v-if="!customAssignee" 
              v-model="taskForm.assignee" 
              placeholder="请选择负责人"
              class="assignee-select"
            >
              <el-option 
                v-for="member in teamMembers" 
                :key="member.id" 
                :label="member.name" 
                :value="member.id" 
              />
            </el-select>
            <el-input 
              v-else 
              v-model="taskForm.customAssigneeName" 
              placeholder="请输入负责人姓名"
              class="assignee-input"
            />
            <el-checkbox v-model="customAssignee" class="custom-checkbox">自定义</el-checkbox>
          </div>
        </el-form-item>
        
        <el-form-item label="截止日期" prop="dueDate" class="form-col">
          <el-date-picker 
            v-model="taskForm.dueDate" 
            type="date" 
            placeholder="请选择截止日期" 
            format="YYYY-MM-DD" 
            value-format="YYYY-MM-DD" 
          />
        </el-form-item>
      </div>
      
      <div class="form-row">
        <el-form-item label="提需人" prop="requester" class="form-col">
          <div class="requester-input">
            <el-select 
              v-if="!customRequester" 
              v-model="taskForm.requester" 
              placeholder="请选择提需人"
              class="requester-select"
            >
              <el-option 
                v-for="member in teamMembers" 
                :key="member.id" 
                :label="member.name" 
                :value="member.id" 
              />
            </el-select>
            <el-input 
              v-else 
              v-model="taskForm.customRequesterName" 
              placeholder="请输入提需人姓名"
              class="requester-input"
            />
            <el-checkbox v-model="customRequester" class="custom-checkbox">自定义</el-checkbox>
          </div>
        </el-form-item>
        
        <el-form-item label="文档链接" class="form-col">
          <el-input 
            v-model="taskForm.documentLink" 
            placeholder="请输入文档链接（如飞书文档、谷歌文档等）" 
          />
        </el-form-item>
      </div>
      
      <el-form-item label="附件">
        <el-upload
          action="#"
          list-type="picture-card"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="5"
        >
          <template #default>
            <i class="el-icon-plus"></i>
          </template>
        </el-upload>
        <div class="upload-tip">支持上传图片、文档等文件，单个文件不超过5MB</div>
      </el-form-item>
      
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'TaskForm',
  props: {
    task: {
      type: Object,
      default: null
    },
    teamMembers: {
      type: Array,
      required: true
    },
    typeOptions: {
      type: Array,
      required: true
    },
    priorityOptions: {
      type: Array,
      required: true
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const formRef = ref(null)
    const customAssignee = ref(false)
    const customRequester = ref(false)
    
    // 初始化表单数据
    const initForm = () => {
      if (props.task) {
        // 编辑模式
        // 检查是否使用自定义负责人
        if (props.task.customAssigneeName) {
          customAssignee.value = true
        }
        
        // 检查是否使用自定义提需人
        if (props.task.customRequesterName) {
          customRequester.value = true
        }
        
        return {
          id: props.task.id,
          name: props.task.name,
          description: props.task.description,
          type: props.task.type,
          priority: props.task.priority,
          assignee: props.task.assignee,
          customAssigneeName: props.task.customAssigneeName || '',
          requester: props.task.requester || '',
          customRequesterName: props.task.customRequesterName || '',
          documentLink: props.task.documentLink || '',
          dueDate: props.task.dueDate,
          attachments: props.task.attachments || []
        }
      } else {
        // 新建模式
        return {
          name: '',
          description: '',
          type: props.typeOptions[0],
          priority: '中',
          assignee: '',
          customAssigneeName: '',
          requester: '',
          customRequesterName: '',
          documentLink: '',
          dueDate: '',
          attachments: []
        }
      }
    }
    
    const taskForm = reactive(initForm())
    
    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入任务名称', trigger: 'blur' },
        { min: 2, max: 50, message: '任务名称长度应在2-50个字符之间', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入任务描述', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择任务类型', trigger: 'change' }
      ],
      priority: [
        { required: true, message: '请选择优先级', trigger: 'change' }
      ],
      assignee: [
        { required: !customAssignee.value, message: '请选择负责人', trigger: 'change' }
      ],
      customAssigneeName: [
        { required: customAssignee.value, message: '请输入负责人姓名', trigger: 'blur' }
      ],
      requester: [
        { required: !customRequester.value, message: '请选择提需人', trigger: 'change' }
      ],
      customRequesterName: [
        { required: customRequester.value, message: '请输入提需人姓名', trigger: 'blur' }
      ]
    }
    
    // 处理文件上传
    const handleFileChange = (file) => {
      // 这里只是模拟文件上传，实际项目中需要实现真正的文件上传逻辑
      if (file.status === 'ready') {
        const fileObj = {
          name: file.name,
          url: URL.createObjectURL(file.raw),
          size: file.size,
          type: file.raw.type
        }
        taskForm.attachments.push(fileObj)
      }
    }
    
    // 提交表单
    const handleSubmit = () => {
      // 根据自定义选项动态调整验证规则
      if (customAssignee.value) {
        rules.assignee[0].required = false
        rules.customAssigneeName[0].required = true
      } else {
        rules.assignee[0].required = true
        rules.customAssigneeName[0].required = false
      }
      
      if (customRequester.value) {
        rules.requester[0].required = false
        rules.customRequesterName[0].required = true
      } else {
        rules.requester[0].required = true
        rules.customRequesterName[0].required = false
      }
      
      formRef.value.validate((valid) => {
        if (valid) {
          // 构建任务数据
          const taskData = {
            ...taskForm,
            hasAttachments: taskForm.attachments.length > 0
          }
          
          // 处理自定义负责人和提需人
          if (customAssignee.value) {
            taskData.assignee = 'custom'
            // 确保customAssigneeName不为空
            if (!taskData.customAssigneeName) {
              return
            }
          } else {
            taskData.customAssigneeName = ''
          }
          
          if (customRequester.value) {
            taskData.requester = 'custom'
            // 确保customRequesterName不为空
            if (!taskData.customRequesterName) {
              return
            }
          } else {
            taskData.customRequesterName = ''
          }
          
          // 如果是新建任务，添加状态和创建时间
          if (!props.task) {
            taskData.status = '未开始'
            taskData.createdAt = new Date().toISOString()
          }
          
          emit('submit', taskData)
        }
      })
    }
    
    // 取消
    const handleCancel = () => {
      emit('cancel')
    }
    
    return {
      formRef,
      taskForm,
      rules,
      customAssignee,
      customRequester,
      handleFileChange,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style lang="scss" scoped>
.task-form {
  padding: 1rem;
  
  .form-row {
    display: flex;
    gap: 1rem;
    
    .form-col {
      flex: 1;
    }
  }
  
  .assignee-input,
  .requester-input {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .assignee-select,
    .requester-select,
    .assignee-input,
    .requester-input {
      flex: 1;
    }
    
    .custom-checkbox {
      margin-left: 8px;
      white-space: nowrap;
    }
  }
  
  .upload-tip {
    font-size: 0.85rem;
    color: var(--text-medium);
    margin-top: 0.5rem;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>