<template>
  <button class="rainbow-button" :class="{ 'disabled': disabled }" :disabled="disabled">
    <slot></slot>
  </button>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RainbowButton',
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  }
})
</script>

<style lang="scss" scoped>
.rainbow-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 0.5rem 1rem;
  background-color: var(--bg-dark);
  border-radius: 0.75rem;
  border: none;
  color: white;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s;
  z-index: 1;
  
  &::before,
  &::after {
    content: '';
    position: absolute;
    left: -2px;
    top: -2px;
    border-radius: 0.75rem;
    background: linear-gradient(45deg, #fb0094, #0000ff, #00ff00, #ffff00, #ff0000, #fb0094, #0000ff, #00ff00, #ffff00, #ff0000);
    background-size: 400%;
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    z-index: -1;
    animation: rainbow 20s linear infinite;
  }
  
  &::after {
    filter: blur(15px);
  }
  
  &:hover::after {
    filter: blur(20px);
  }
  
  &:active {
    transform: scale(0.95);
  }
  
  &.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    
    &::before,
    &::after {
      animation: none;
      opacity: 0.5;
    }
    
    &:active {
      transform: none;
    }
  }
}

@keyframes rainbow {
  0% { background-position: 0 0; }
  50% { background-position: 400% 0; }
  100% { background-position: 0 0; }
}
</style>