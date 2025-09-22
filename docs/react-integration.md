# React 组件集成指南

## 当前项目状态

当前项目是一个基于 Vue 3 的应用程序，使用以下技术栈：

- Vue 3
- Vue Router
- Pinia (状态管理)
- SCSS
- Element Plus

项目**不支持**以下 React 组件所需的技术：

- React
- TypeScript
- Tailwind CSS
- shadcn UI 组件库

## 集成 React 组件的方案

### 方案1：在 Vue 项目中使用 React 组件（推荐）

要在当前 Vue 项目中使用 React 组件，需要进行以下设置：

1. 安装必要的依赖：

```bash
npm install react react-dom @vitejs/plugin-react
npm install -D typescript @types/react @types/react-dom
npm install -D tailwindcss postcss autoprefixer
```

2. 创建 TypeScript 配置文件 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

3. 创建 `tsconfig.node.json`：

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

4. 配置 Tailwind CSS：

创建 `tailwind.config.js`：

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

创建 `postcss.config.js`：

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

5. 更新 Vite 配置以支持 React：

将 `vite.config.js` 更新为 `vite.config.ts`，并添加 React 插件：

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [vue(), react()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
```

6. 创建 React 组件包装器：

创建一个 Vue 组件来包装 React 组件：

```vue
<!-- src/components/ReactWrapper.vue -->
<template>
  <div ref="reactRoot"></div>
</template>

<script>
import { defineComponent, onMounted, onBeforeUnmount, ref } from 'vue'
import ReactDOM from 'react-dom/client'

export default defineComponent({
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
    const reactRoot = ref(null)
    let root = null

    onMounted(() => {
      const { component, props: componentProps } = props
      root = ReactDOM.createRoot(reactRoot.value)
      root.render(React.createElement(component, componentProps))
    })

    onBeforeUnmount(() => {
      if (root) {
        root.unmount()
      }
    })

    return {
      reactRoot
    }
  }
})
</script>
```

### 方案2：将项目迁移到 React（长期方案）

如果计划长期使用 React 和 shadcn UI，建议考虑将项目逐步迁移到 React：

1. 创建一个新的 React 项目，使用 Next.js 或 Vite
2. 安装并配置 Tailwind CSS 和 shadcn UI
3. 逐步将 Vue 组件迁移到 React 组件
4. 使用路由系统（如 React Router 或 Next.js 路由）替换 Vue Router

## 彩虹边框按钮组件集成

要集成提供的彩虹边框按钮组件，请按照以下步骤操作：

1. 创建组件目录结构：

```
src/
  components/
    ui/
      rainbow-borders-button.tsx
    react/
      demo.tsx
```

2. 将提供的 React 组件代码复制到相应文件中

3. 创建一个 Vue 包装器组件来使用这个 React 组件：

```vue
<!-- src/components/ui/RainbowButtonWrapper.vue -->
<template>
  <ReactWrapper :component="RainbowButton" :props="buttonProps" />
</template>

<script>
import { defineComponent } from 'vue'
import ReactWrapper from '../ReactWrapper.vue'
import { Button as RainbowButton } from '../ui/rainbow-borders-button'

export default defineComponent({
  name: 'RainbowButtonWrapper',
  components: {
    ReactWrapper
  },
  props: {
    text: {
      type: String,
      default: 'Button'
    }
  },
  setup(props) {
    const buttonProps = {
      text: props.text
    }

    return {
      RainbowButton,
      buttonProps
    }
  }
})
</script>
```

## 注意事项

1. 在 Vue 项目中集成 React 组件会增加项目的复杂性和包大小
2. 需要维护两套不同的组件系统和样式方案
3. 可能会遇到状态管理和事件处理的兼容性问题
4. 建议长期规划是选择一种技术栈并逐步迁移

## 替代方案：使用纯 Vue 实现类似效果

考虑到当前项目是纯 Vue 项目，一个更简单的方案是使用 Vue 和 SCSS 重新实现彩虹边框按钮效果，这样可以避免引入 React 依赖。

我们已经在项目中实现了类似的彩虹边框效果，应用于所有按钮。如果需要更多自定义，可以进一步扩展现有的 CSS 样式。