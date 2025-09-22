# 彩虹边框按钮效果与React组件集成指南

## 彩虹边框按钮效果

本项目已经实现了彩虹边框按钮效果，并应用于所有按钮。效果包括：

1. 彩虹渐变边框
2. 边框动画效果
3. 悬停时的模糊效果增强
4. 点击时的缩放效果

### 如何使用

有两种方式使用彩虹边框按钮效果：

#### 1. 使用btn类

为任何按钮添加`btn`类即可应用彩虹边框效果：

```html
<button class="btn">彩虹按钮</button>
```

可以与其他按钮类结合使用：

```html
<button class="btn btn-primary">主要按钮</button>
<button class="btn btn-info">信息按钮</button>
```

#### 2. 使用RainbowButton组件

使用专门的RainbowButton组件：

```html
<template>
  <RainbowButton>彩虹按钮</RainbowButton>
  <RainbowButton disabled>禁用状态</RainbowButton>
</template>

<script>
import RainbowButton from '@/components/ui/RainbowButton.vue'

export default {
  components: {
    RainbowButton
  }
}
</script>
```

### 按钮演示页面

项目中包含一个按钮演示页面，可以查看所有按钮效果：

- 路径：`/button-demo`
- 文件：`src/views/ButtonDemoView.vue`

## React组件集成

本项目提供了React组件集成的参考实现，但当前项目是基于Vue 3的，需要额外配置才能使用React组件。

### 集成文档

详细的React组件集成指南请参考：

- 文档：`docs/react-integration.md`

### 示例文件

项目中包含以下React组件示例文件：

- React包装器：`src/components/ReactWrapper.vue`
- 彩虹边框按钮组件：`src/components/ui/rainbow-borders-button.tsx`
- 演示组件：`src/components/react/demo.tsx`

这些文件仅作为参考，需要安装React、TypeScript和Tailwind CSS才能正常使用。

### 推荐方案

对于当前项目，推荐使用Vue实现的彩虹边框按钮效果，而不是引入React依赖。如果未来需要使用更多React组件，可以考虑逐步迁移到React或使用混合方案。