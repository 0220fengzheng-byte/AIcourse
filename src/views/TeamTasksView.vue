<template>
  <div class="team-tasks-view">
    <h1 class="page-title">🎯 团队任务管理</h1>
    <FunctionNav />
    <TaskManagement />
  </div>
</template>

<script>
import TaskManagement from '@/components/team-tasks/TaskManagement.vue'
import FunctionNav from '@/components/ui/FunctionNav.vue'

export default {
  name: 'TeamTasksView',
  components: {
    TaskManagement,
    FunctionNav
  }
}
</script>

<style lang="scss" scoped>
.team-tasks-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
}
</style>