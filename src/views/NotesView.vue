<template>
  <div class="notes-view">
    <h1 class="page-title">📝 AI记事本</h1>
    
    <FunctionNav />
    
    <div class="notes-container">
      <!-- 左侧笔记列表 -->
      <div class="notes-sidebar rainbow-card">
        <div class="sidebar-header">
          <h3>我的笔记</h3>
          <button class="add-note-btn" @click="createNewNote">+ 新建笔记</button>
        </div>
        
        <div class="notes-list">
          <div 
            v-for="note in notes" 
            :key="note.id"
            :class="['note-item', selectedNote && selectedNote.id === note.id ? 'active' : '']"
            @click="selectNote(note)"
          >
            <div class="note-title">{{ note.title }}</div>
            <div class="note-preview">{{ note.content.substring(0, 50) }}{{ note.content.length > 50 ? '...' : '' }}</div>
            <div class="note-date">{{ formatDate(note.createdAt) }}</div>
          </div>
          
          <div v-if="notes.length === 0" class="empty-notes">
            <p>暂无笔记，点击"新建笔记"开始创建</p>
          </div>
        </div>
      </div>
      
      <!-- 右侧编辑区 -->
      <div class="notes-editor rainbow-card" v-if="selectedNote">
        <div class="editor-header">
          <input 
            type="text" 
            class="note-title-input" 
            v-model="selectedNote.title" 
            placeholder="笔记标题"
            @input="updateNote"
          >
          <div class="editor-actions">
            <button class="delete-btn" @click="deleteNote">删除</button>
          </div>
        </div>
        
        <textarea 
          class="note-content-input" 
          v-model="selectedNote.content" 
          placeholder="在这里输入笔记内容..."
          @input="updateNote"
        ></textarea>
      </div>
      
      <!-- 空状态 -->
      <div class="empty-state rainbow-card" v-if="!selectedNote">
        <div class="empty-icon">📝</div>
        <h3>选择或创建一个笔记</h3>
        <p>点击左侧的笔记查看详情，或创建一个新笔记开始记录</p>
        <button class="create-note-btn" @click="createNewNote">+ 新建笔记</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import FunctionNav from '@/components/ui/FunctionNav.vue'

export default {
  name: 'NotesView',
  components: {
    FunctionNav
  },
  
  setup() {
    const notes = ref([])
    const selectedNote = ref(null)
    
    // 从本地存储加载笔记
    const loadNotes = () => {
      const savedNotes = localStorage.getItem('notes')
      if (savedNotes) {
        notes.value = JSON.parse(savedNotes)
      }
    }
    
    // 保存笔记到本地存储
    const saveNotes = () => {
      localStorage.setItem('notes', JSON.stringify(notes.value))
    }
    
    // 选择笔记
    const selectNote = (note) => {
      selectedNote.value = { ...note }
    }
    
    // 创建新笔记
    const createNewNote = () => {
      const newNote = {
        id: Date.now().toString(),
        title: '新笔记',
        content: '',
        createdAt: new Date(),
        updatedAt: new Date()
      }
      
      notes.value.unshift(newNote)
      saveNotes()
      selectNote(newNote)
    }
    
    // 更新笔记
    const updateNote = () => {
      if (!selectedNote.value) return
      
      selectedNote.value.updatedAt = new Date()
      
      const index = notes.value.findIndex(note => note.id === selectedNote.value.id)
      if (index !== -1) {
        notes.value[index] = { ...selectedNote.value }
        saveNotes()
      }
    }
    
    // 删除笔记
    const deleteNote = () => {
      if (!selectedNote.value) return
      
      if (confirm('确定要删除这个笔记吗？')) {
        notes.value = notes.value.filter(note => note.id !== selectedNote.value.id)
        saveNotes()
        selectedNote.value = null
      }
    }
    
    // 格式化日期
    const formatDate = (date) => {
      const d = new Date(date)
      return d.toLocaleDateString()
    }
    
    onMounted(() => {
      loadNotes()
    })
    
    return {
      notes,
      selectedNote,
      selectNote,
      createNewNote,
      updateNote,
      deleteNote,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.notes-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .notes-container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 1.5rem;
    height: 70vh;
    
    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }
  
  .notes-sidebar {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid var(--text-light);
      
      h3 {
        margin: 0;
      }
      
      .add-note-btn {
        background: var(--primary-green);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        
        &:hover {
          background: darken(#00b894, 10%);
        }
      }
    }
    
    .notes-list {
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem;
      
      .note-item {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
        
        &:hover {
          background-color: rgba(0, 0, 0, 0.05);
        }
        
        &.active {
          background-color: rgba(0, 184, 148, 0.1);
          border-left: 3px solid var(--primary-green);
        }
        
        .note-title {
          font-weight: bold;
          margin-bottom: 0.5rem;
          color: var(--text-dark);
        }
        
        .note-preview {
          font-size: 0.9rem;
          color: var(--text-medium);
          margin-bottom: 0.5rem;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        
        .note-date {
          font-size: 0.8rem;
          color: var(--text-light);
        }
      }
      
      .empty-notes {
        padding: 2rem;
        text-align: center;
        color: var(--text-medium);
      }
    }
  }
  
  .notes-editor {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .editor-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid var(--text-light);
      
      .note-title-input {
        flex: 1;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        padding: 0.5rem;
        background: transparent;
        
        &:focus {
          outline: none;
        }
      }
      
      .editor-actions {
        .delete-btn {
          background: var(--danger);
          color: white;
          border: none;
          border-radius: 4px;
          padding: 0.5rem 1rem;
          cursor: pointer;
          
          &:hover {
            background: darken(#e84393, 10%);
          }
        }
      }
    }
    
    .note-content-input {
      flex: 1;
      padding: 1rem;
      border: none;
      resize: none;
      font-family: inherit;
      font-size: 1rem;
      line-height: 1.5;
      
      &:focus {
        outline: none;
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    text-align: center;
    
    .empty-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      color: var(--primary-green);
    }
    
    h3 {
      color: var(--text-dark);
      margin-bottom: 0.5rem;
    }
    
    p {
      color: var(--text-medium);
      margin-bottom: 1.5rem;
    }
    
    .create-note-btn {
      background: var(--primary-green);
      color: white;
      border: none;
      border-radius: 4px;
      padding: 0.75rem 1.5rem;
      cursor: pointer;
      font-size: 1rem;
      
      &:hover {
        background: darken(#00b894, 10%);
      }
    }
  }
}
</style>