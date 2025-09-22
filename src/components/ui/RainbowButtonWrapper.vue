<template>
  <RainbowButton>
    {{ text }}
  </RainbowButton>
</template>

<script>
import { defineComponent } from 'vue'
import RainbowButton from './RainbowButton.vue'

export default defineComponent({
  name: 'RainbowButtonWrapper',
  components: {
    RainbowButton
  },
  props: {
    text: {
      type: String,
      default: 'Button'
    }
  }
})
</script>