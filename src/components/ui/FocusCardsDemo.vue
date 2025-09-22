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
        src: "https://img.freepik.com/free-vector/chat-bot-concept-illustration_114360-5522.jpg",
        path: "/chat",
        description: "与AI助手对话，获取学习帮助和建议"
      },
      {
        title: "智能记事本",
        src: "https://img.freepik.com/free-vector/notebook-concept-illustration_114360-387.jpg",
        path: "/notes",
        description: "记录笔记，AI自动分析和标签生成"
      },
      {
        title: "待办事项",
        src: "https://img.freepik.com/free-vector/checklist-concept-illustration_114360-479.jpg",
        path: "/todo",
        description: "管理个人任务，设置优先级和截止时间"
      },
      {
        title: "番茄钟",
        src: "https://img.freepik.com/free-vector/time-management-concept-illustration_114360-1013.jpg",
        path: "/pomodoro",
        description: "使用番茄工作法提高专注力和效率"
      },
      {
        title: "团队任务",
        src: "https://img.freepik.com/free-vector/team-concept-illustration_114360-678.jpg",
        path: "/team-tasks",
        description: "协作管理团队任务，跟踪进度和状态"
      },
      {
        title: "设置",
        src: "https://img.freepik.com/free-vector/settings-concept-illustration_114360-3754.jpg",
        path: "/settings",
        description: "自定义应用设置和个人偏好"
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