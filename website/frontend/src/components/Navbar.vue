<script setup lang="ts">
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import { Button } from '@/components/ui/button'
import { Github } from 'lucide-vue-next'
</script>

<template>
  <header class="border-b border-slate-200 bg-white">
    <div class="container mx-auto flex h-16 items-center justify-between px-4">
      <router-link to="/" class="text-2xl font-bold text-slate-800 hover:text-slate-600 transition-colors">
        MetHMMDB
      </router-link>
      
      <div class="flex items-center space-x-4">
        <router-link to="/browse">
          <Button variant="ghost" class="text-slate-700">
            Browse Models
          </Button>
        </router-link>
        
        <router-link to="/download">
          <Button variant="ghost" class="text-slate-700">
            Download
          </Button>
        </router-link>
        
        <router-link to="/about">
          <Button variant="ghost" class="text-slate-700">
            About
          </Button>
        </router-link>
        
        <a 
          href="https://github.com/Haelmorn/MetHMMDB" 
          target="_blank"
          rel="noopener noreferrer"
          aria-label="GitHub Repository"
        >
          <Button variant="ghost" size="icon" class="text-slate-700">
            <Github class="h-5 w-5" />
          </Button>
        </a>
      </div>
    </div>
  </header>
</template>
