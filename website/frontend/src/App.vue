<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <router-view />
  </div>
</template>
