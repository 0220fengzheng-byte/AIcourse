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
      <img 
        :src="card.src" 
        :alt="card.title" 
        class="card-image"
      />
      <div 
        class="card-overlay"
        :class="{ 'visible': hovered === index }"
      >
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
  background-color: #f3f4f6;
  border-radius: 0.5rem;
  overflow: hidden;
  height: 15rem;
  width: 100%;
  transition: all 0.3s ease-out;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.5s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  }

  @media (min-width: 768px) {
    height: 24rem;
  }

  &.blur-scale {
    filter: blur(4px);
    transform: scale(0.98);
  }
}

.card-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding: 2rem 1rem;
  opacity: 0;
  transition: opacity 0.3s ease;
  text-align: center;

  &.visible {
    opacity: 1;
  }
}

.card-title {
  font-size: 1.25rem;
  font-weight: 500;
  background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  text-align: center;

  @media (min-width: 768px) {
    font-size: 1.5rem;
  }
}

.card-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
  width: 100%;
  margin: 0.5rem 0 0;
  text-align: center;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  
  @media (max-width: 768px) {
    font-size: 0.8rem;
    -webkit-line-clamp: 2;
  }
}
</style>