<template>
  <div class="grid-container">
    <div 
      v-for="(card, index) in cards" 
      :key="card.title"
      class="card"
      :class="{ 'blur-scale': hovered !== null && hovered !== index }"
      @mouseenter="setHovered(index)"
      @mouseleave="setHovered(null)"
      @click="handleCardClick(index)"
    >
      <div class="card-icon-wrapper">
        <div class="card-icon">{{ card.icon }}</div>
      </div>
      <div class="card-content">
        <div class="card-title">
          {{ card.title }}
        </div>
        <p v-if="card.description" class="card-description">{{ card.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'FocusCards',
  props: {
    cards: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  emits: ['card-click'],
  setup(props, { emit }) {
    const hovered = ref(null);

    const setHovered = (index) => {
      hovered.value = index;
    };
    
    const handleCardClick = (index) => {
      emit('card-click', index);
    };

    return {
      hovered,
      setHovered,
      handleCardClick
    };
  }
}
</script>

<style lang="scss" scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 2.5rem;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  padding: 0 1rem;

  @media (min-width: 768px) {
    grid-template-columns: repeat(3, 1fr);
    padding: 0 2rem;
  }
}

.card {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1rem;
  overflow: hidden;
  height: 12rem;
  width: 100%;
  transition: all 0.3s ease-out;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.5s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1.5rem;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  }

  @media (min-width: 768px) {
    height: 14rem;
    padding: 2rem;
  }

  &.blur-scale {
    filter: blur(4px);
    transform: scale(0.98);
  }
}

.card-icon-wrapper {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon {
  font-size: 3rem;
  line-height: 1;
  filter: drop-shadow(0 4px 8px rgba(25, 118, 210, 0.2));

  @media (min-width: 768px) {
    font-size: 3.5rem;
  }
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

  @media (min-width: 768px) {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
}

.card-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.95);
  width: 100%;
  margin: 0;
  text-align: center;
  line-height: 1.4;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);

  @media (max-width: 768px) {
    font-size: 0.8rem;
  }
}
</style>