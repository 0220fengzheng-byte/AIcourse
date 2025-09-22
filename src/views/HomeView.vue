<template>
  <div class="home-view">
    <div class="welcome-section rainbow-card">
      <h1>🎨 奇妙AI之旅</h1>
      <p class="subtitle">AI与你同行</p>
    </div>
    
    <div class="focus-cards-section">
      <FocusCardsDemo />
    </div>
  </div>
</template>

<script>
import FocusCardsDemo from '@/components/ui/FocusCardsDemo.vue';

export default {
  name: 'HomeView',
  components: {
    FocusCardsDemo
  }
}
</script>

<style lang="scss" scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-section {
  text-align: center;
  padding: 3rem 2.5rem;
  margin-bottom: 1rem;
  
  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--primary-blue);
  }
  
  .subtitle {
    font-size: 1.5rem;
    color: var(--text-medium);
    font-weight: 500;
    margin: 0 auto;
    letter-spacing: 1px;
  }
}

.focus-cards-section {
  margin: 1rem 0 3rem;
}
</style>