<template>
  <div ref="reactRoot"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import React from 'react';
import ReactDOM from 'react-dom/client';

export default {
  name: 'ReactWrapper',
  props: {
    component: {
      type: Object,
      required: true
    },
    props: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const reactRoot = ref(null);
    let root = null;

    onMounted(() => {
      const { component, props: componentProps } = props;
      root = ReactDOM.createRoot(reactRoot.value);
      root.render(React.createElement(component, componentProps));
    });

    onBeforeUnmount(() => {
      if (root) {
        root.unmount();
      }
    });

    return {
      reactRoot
    };
  }
};
</script>