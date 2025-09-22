<template>
  <div class="rainbow-button-demo">
    <h1>彩虹边框按钮演示</h1>
    <div class="demo-container">
      <h2>React 组件版本</h2>
      <RainbowButtonWrapper text="React 按钮" />
      
      <h2>Vue 组件版本</h2>
      <RainbowButton>Vue 按钮</RainbowButton>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import RainbowButtonWrapper from '@/components/ui/RainbowButtonWrapper.vue'
import RainbowButton from '@/components/ui/RainbowButton.vue'

export default defineComponent({
  name: 'RainbowButtonDemo',
  components: {
    RainbowButtonWrapper,
    RainbowButton
  }
})
</script>

<style lang="scss" scoped>
.rainbow-button-demo {
  padding: 2rem;
  
  h1 {
    margin-bottom: 2rem;
    text-align: center;
  }
  
  .demo-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    
    h2 {
      margin-bottom: 1rem;
    }
  }
}
</style>