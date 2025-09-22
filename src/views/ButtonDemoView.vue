<template>
  <div class="button-demo-view">
    <h1 class="page-title">🌈 按钮特效演示</h1>
    
    <FunctionNav />
    
    <div class="demo-container rainbow-card">
      <h2>彩虹边框按钮效果</h2>
      
      <div class="button-section">
        <h3>标准按钮</h3>
        <div class="button-row">
          <button>标准按钮</button>
          <button class="btn-primary">主要按钮</button>
          <button class="btn-info">信息按钮</button>
          <button class="btn-success">成功按钮</button>
          <button class="btn-warning">警告按钮</button>
          <button class="btn-danger">危险按钮</button>
        </div>
      </div>
      
      <div class="button-section">
        <h3>自定义彩虹按钮组件</h3>
        <div class="button-row">
          <RainbowButton>彩虹按钮</RainbowButton>
          <RainbowButton disabled>禁用状态</RainbowButton>
        </div>
      </div>
      
      <div class="button-section">
        <h3>应用场景示例</h3>
        <div class="button-row">
          <button>登录</button>
          <button>注册</button>
          <button>提交</button>
          <button>保存</button>
          <button>取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import FunctionNav from '@/components/ui/FunctionNav.vue'
import RainbowButton from '@/components/ui/RainbowButton.vue'

export default defineComponent({
  name: 'ButtonDemoView',
  components: {
    FunctionNav,
    RainbowButton
  }
})
</script>

<style lang="scss" scoped>
.button-demo-view {
  .page-title {
    margin-bottom: 1.5rem;
    color: var(--text-dark);
  }
  
  .demo-container {
    padding: 2rem;
    margin-bottom: 2rem;
    
    h2 {
      margin-top: 0;
      margin-bottom: 1.5rem;
      color: var(--text-dark);
    }
  }
  
  .button-section {
    margin-bottom: 2rem;
    
    h3 {
      margin-bottom: 1rem;
      color: var(--text-dark);
      font-size: 1.2rem;
    }
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .button-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
  }
}
</style>