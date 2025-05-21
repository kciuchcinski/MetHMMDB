<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Database, Download, Search } from "lucide-vue-next";
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-slate-50">

    <main class="container mx-auto px-4 py-12">
      <!-- Hero Section -->
      <div class="flex flex-col items-center justify-center text-center mb-16">
        <h1 class="text-5xl font-bold mb-6 text-slate-800">MetHMMDB</h1>

        <p class="text-lg text-slate-700 mb-8 max-w-2xl leading-relaxed">
          MetHMMDb contains
          <span class="font-semibold text-slate-900"
            >254 profile Hidden Markov Models</span
          >
          covering 121 microbial MMRGs and their functions. Developed through
          iterative database searches, sequence clustering, structural
          prediction, and manual curation, MetHMMDb prioritizes functional
          annotation for accurate gene detection and classification.
        </p>

        <div class="flex flex-wrap gap-4 justify-center">
          <Button size="lg" class="gap-2" asChild>
            <router-link to="/browse">
              <Search class="w-5 h-5" />
              Browse Models
            </router-link>
          </Button>

          <Button size="lg" variant="outline" class="gap-2" asChild>
            <router-link to="/download">
              <Download class="w-5 h-5" />
              Download
            </router-link>
          </Button>
        </div>
      </div>

      <!-- Feature Cards -->
      <div class="grid md:grid-cols-3 gap-6 mt-12">
        <Card class="transition-all hover:shadow-md">
          <CardContent class="pt-6">
            <div
              class="rounded-full bg-slate-100 p-3 w-12 h-12 flex items-center justify-center mb-4"
            >
              <Database class="w-6 h-6 text-slate-600" />
            </div>
            <h3 class="text-xl font-semibold mb-2 text-slate-800">
              254 HMM Profiles
            </h3>
            <p class="text-slate-600">
              Access a comprehensive database of Hidden Markov Models for
              microbial gene analysis.
            </p>
          </CardContent>
        </Card>

        <Card class="transition-all hover:shadow-md">
          <CardContent class="pt-6">
            <div
              class="rounded-full bg-slate-100 p-3 w-12 h-12 flex items-center justify-center mb-4"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6 text-slate-600"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2 text-slate-800">
              Accurate Detection
            </h3>
            <p class="text-slate-600">
              Prioritizes functional annotation for precise gene detection and
              classification.
            </p>
          </CardContent>
        </Card>

        <Card class="transition-all hover:shadow-md">
          <CardContent class="pt-6">
            <div
              class="rounded-full bg-slate-100 p-3 w-12 h-12 flex items-center justify-center mb-4"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6 text-slate-600"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
                ></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2 text-slate-800">
              Research-Driven
            </h3>
            <p class="text-slate-600">
              Developed through rigorous database searches, clustering, and
              manual curation.
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Citation Section -->
      <Card class="mt-16 border-slate-200 bg-slate-50">
        <CardContent class="pt-6 pb-6 text-center">
          <h3 class="text-xl font-semibold mb-2 text-slate-800">
            Cite This Work
          </h3>
          <p
            class="text-slate-700 font-mono text-sm bg-white p-3 rounded border border-slate-200 inline-block"
          >
            Ciuchcinski, K. & Dziurzynski, M. (2025) Fast and accurate detection
            of metal resistance genes using MetHMMDb. <i>bioRxiv</i>,
            10.1101/2024.12.26.629440
          </p>
        </CardContent>
      </Card>
    </main>
  </div>
</template>
