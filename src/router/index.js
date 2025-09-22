import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('../views/ChatView.vue')
  },
  {
    path: '/notes',
    name: 'notes',
    component: () => import('../views/NotesView.vue')
  },
  {
    path: '/todo',
    name: 'todo',
    component: () => import('../views/TodoView.vue')
  },
  {
    path: '/pomodoro',
    name: 'pomodoro',
    component: () => import('../views/PomodoroView.vue')
  },
  {
    path: '/team-tasks',
    name: 'team-tasks',
    component: () => import('../views/TeamTasksView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/SettingsView.vue')
  },
  {    path: '/button-demo',    name: 'button-demo',    component: () => import('../views/ButtonDemoView.vue')  },
  {    path: '/rainbow-button',    name: 'rainbow-button',    component: () => import('../views/RainbowButtonDemo.vue')  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router