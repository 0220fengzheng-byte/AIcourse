<template>
  <FocusCards :cards="cards" @card-click="navigateTo" />
</template>

<script>
import FocusCards from './FocusCards.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'FocusCardsDemo',
  components: {
    FocusCards
  },
  setup() {
    const router = useRouter();
    
    const cards = ref([
      {
        title: "AI对话",
        icon: "💬",
        path: "/chat",
        description: "与AI助手对话，获取学习帮助和建议，解答疑难问题"
      },
      {
        title: "智能记事本",
        icon: "📝",
        path: "/notes",
        description: "记录笔记，AI自动分析和标签生成，智能整理知识点"
      },
      {
        title: "待办事项",
        icon: "✅",
        path: "/todo",
        description: "管理个人任务，设置优先级和截止时间，提高工作效率"
      },
      {
        title: "番茄钟",
        icon: "🍅",
        path: "/pomodoro",
        description: "使用番茄工作法提高专注力和效率，科学管理时间"
      },
      {
        title: "团队任务",
        icon: "👥",
        path: "/team-tasks",
        description: "协作管理团队任务，跟踪进度和状态，提升团队协作效率"
      },
      {
        title: "设置",
        icon: "⚙️",
        path: "/settings",
        description: "自定义应用设置和个人偏好，打造专属工作环境"
      }
    ]);

    const navigateTo = (index) => {
      const card = cards.value[index];
      if (card && card.path) {
        router.push(card.path);
      }
    };

    return {
      cards,
      navigateTo
    };
  }
}
</script>