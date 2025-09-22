<template>
  <div class="function-nav">
    <div class="function-nav-container">
      <router-link 
        v-for="item in navItems" 
        :key="item.path" 
        :to="item.path"
        class="nav-item"
        :class="{ 'active': currentPath === item.path }"
      >
        <div class="nav-icon">{{ item.icon }}</div>
        <div class="nav-title">{{ item.title }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'FunctionNav',
  setup() {
    const route = useRoute();
    const currentPath = computed(() => route.path);
    
    const navItems = [
      { title: 'AI对话', path: '/chat', icon: '🤖' },
      { title: '记事本', path: '/notes', icon: '📝' },
      { title: '待办事项', path: '/todo', icon: '✅' },
      { title: '番茄钟', path: '/pomodoro', icon: '🍅' },
      { title: '团队任务', path: '/team-tasks', icon: '🎯' },
    ];
    
    return {
      navItems,
      currentPath
    };
  }
};
</script>

<style lang="scss" scoped>
.function-nav {
  margin: 0.5rem 0 1.5rem;
}

.function-nav-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  background-color: var(--bg-white);
  padding: 0.75rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--text-medium);
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  position: relative;
  z-index: 1;
  background-color: var(--bg-white);
  
  &::before,
  &::after {
    content: '';
    position: absolute;
    left: -2px;
    top: -2px;
    border-radius: 0.6rem;
    background: linear-gradient(45deg, #fb0094, #0000ff, #00ff00, #ffff00, #ff0000, #fb0094, #0000ff, #00ff00, #ffff00, #ff0000);
    background-size: 400%;
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    z-index: -1;
    animation: rainbow 20s linear infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &::after {
    filter: blur(8px);
  }
  
  &:hover, &.active {
    color: var(--primary-blue);
    
    &::before,
    &::after {
      opacity: 1;
    }
  }
}

.nav-icon {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.nav-title {
  font-size: 0.9rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .function-nav-container {
    gap: 0.5rem;
  }
  
  .nav-item {
    padding: 0.5rem 0.75rem;
  }
  
  .nav-icon {
    font-size: 1.25rem;
  }
  
  .nav-title {
    font-size: 0.8rem;
  }
}
</style>