<template>
  <div class="app-container crayon-style">    
    <main class="app-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
@import './assets/styles/variables.scss';

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', sans-serif;
  background-color: var(--bg-light);
  color: var(--text-dark);
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}



.app-content {
  flex-grow: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.crayon-style {
  --border-radius: 12px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  
  .rainbow-card {
    background-color: var(--bg-white);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(
        to right,
        var(--primary-blue),
        var(--primary-green),
        var(--primary-yellow),
        var(--primary-pink)
      );
    }
  }
}
</style>