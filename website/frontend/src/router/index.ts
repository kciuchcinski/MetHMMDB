import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/components/LandingPage.vue'
import Downloads from '@/components/Downloads.vue'
import BrowseModels from '@/components/BrowseModels.vue'
import About from '@/components/About.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage
  },
  {
    path: '/download',
    name: 'Downloads',
    component: Downloads
  },
  // Add placeholder routes for other pages
  {
    path: '/browse',
    name: 'Browse',
    component: BrowseModels
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
