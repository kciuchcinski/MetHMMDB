<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { FileText, Database, GitBranch, BookOpen } from "lucide-vue-next";
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="space-y-8 max-w-4xl mx-auto">
      <!-- About Section -->
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 mb-4">
          About MetHMMDB
        </h1>
        <p class="text-slate-600 mb-6">
          MetHMMDB is a database containing 254 profile Hidden Markov Models
          representing 121 microbial metal resistance genes (MMRGs). Unlike
          traditional sequence-based resources, MetHMMDB relies on HMMs to
          improve detection sensitivity and functional specificity across
          microbial communities.
        </p>

        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <Database class="h-5 w-5" />
                Database Overview
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul class="space-y-2 text-slate-600">
                <li>• 254 profile Hidden Markov Models</li>
                <li>• Covers 121 microbial metal resistance genes</li>
                <li>• Created through iterative database searches</li>
                <li>
                  • Emphasizes functional annotation over gene classification
                </li>
                <li>
                  • Superior detection sensitivity compared to sequence-based
                  methods
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <FileText class="h-5 w-5" />
                Key Features
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul class="space-y-2 text-slate-600">
                <li>• Improved sensitivity in detecting distant homologs</li>
                <li>• Captures position-specific amino acid preferences</li>
                <li>• Incorporates structural information</li>
                <li>• Outperforms sequence-based approaches</li>
                <li>
                  • Identifies over twice as many MMRGs in metagenomic datasets
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      <Separator />

      <!-- Construction Section -->
      <div>
        <h2 class="text-2xl font-bold text-slate-900 mb-4">
          Database Construction
        </h2>
        <p class="text-slate-600 mb-6">
          MetHMMDB was constructed through a systematic, multi-step process
          starting with experimentally confirmed metal resistance genes.
        </p>

        <Card class="mb-6">
          <CardContent class="pt-6">
            <ol class="space-y-4 text-slate-600">
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >1</span
                >
                <span
                  >Started with 374 experimentally confirmed metal resistance
                  genes from the MetGeneDB database</span
                >
              </li>
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >2</span
                >
                <span
                  >Performed DIAMOND BLASTP searches against SwissProt using
                  stringent criteria (>90% identity and coverage)</span
                >
              </li>
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >3</span
                >
                <span
                  >Searched the NCBI NR database, bringing the final dataset to
                  11,025 proteins</span
                >
              </li>
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >4</span
                >
                <span
                  >Clustered sequences using MMseqs2 with optimized
                  parameters</span
                >
              </li>
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >5</span
                >
                <span
                  >Performed comprehensive functional annotation using domain
                  detection, protein structure prediction, and structural
                  similarity searches</span
                >
              </li>
              <li class="flex gap-3">
                <span
                  class="bg-slate-100 rounded-full h-6 w-6 flex items-center justify-center text-slate-700 font-medium flex-shrink-0"
                  >6</span
                >
                <span
                  >Generated multiple sequence alignments using MAFFT and
                  converted to profile HMMs using HMMER3</span
                >
              </li>
            </ol>
          </CardContent>
        </Card>
      </div>

      <Separator />

      <!-- Usage Section -->
      <div>
        <h2 class="text-2xl font-bold text-slate-900 mb-4">
          Usage Instructions
        </h2>
        <p class="text-slate-600 mb-6">
          The database was designed to be used with HMMER suite tools like
          <code class="bg-slate-100 px-2 py-1 rounded font-mono">hmmscan</code>
          and
          <code class="bg-slate-100 px-2 py-1 rounded font-mono">hmmsearch</code
          >.
        </p>

        <Card class="mb-6">
          <CardHeader>
            <CardTitle>Installation</CardTitle>
            <CardDescription
              >Before starting, download the data and ensure you have HMMER
              installed</CardDescription
            >
          </CardHeader>
          <CardContent>
            <pre class="bg-slate-100 p-4 rounded-md overflow-x-auto text-sm">
# Download the latest release from our website
# https://methmmdb.com/download

# Or directly from GitHub releases
wget https://github.com/Haelmorn/MetHMMDB/releases/download/v1.0/methmmdb_v1.0.hmm

# Ensure HMMER suite is installed on your system
# For Ubuntu/Debian:
sudo apt-get install hmmer

# For macOS:
brew install hmmer</pre>
          </CardContent>
        </Card>

        <Card class="mb-6">
          <CardHeader>
            <CardTitle>Basic Usage</CardTitle>
            <CardDescription
              >Examples of how to use the database with HMMER
              tools</CardDescription
            >
          </CardHeader>
          <CardContent>
            <pre class="bg-slate-100 p-4 rounded-md overflow-x-auto text-sm">
# Using hmmscan to search sequences against MetHMMDB
hmmscan --domtblout output.tbl path/to/MetHMMDB/methmmdb_v1.0.hmm query_sequences.fasta

# Using hmmsearch to search MetHMMDB profiles against a sequence database
hmmsearch --domtblout output.tbl path/to/MetHMMDB/methmmdb_v1.0.hmm sequence_database.fasta</pre
            >
          </CardContent>
        </Card>

        <p class="text-slate-600 mb-4">
          Additionally, since reading the output files can be tricky, the
          <a
            href="https://github.com/EnzoAndree/HmmPy"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-600 hover:underline"
            >HmmPy</a
          >
          package can be used to turn the
          <code class="bg-slate-100 px-2 py-1 rounded font-mono"
            >--domtblout</code
          >
          file into a nice
          <code class="bg-slate-100 px-2 py-1 rounded font-mono">.tsv</code>
          that's easy to parse by your favorite tool.
        </p>

        <p class="text-slate-600">
          For more detailed usage, including output options, we recommend
          reading the
          <a
            href="http://hmmer.org/documentation.html"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-600 hover:underline"
            >HMMER suite documentation and User's guide</a
          >.
        </p>
      </div>

      <Separator />

      <!-- Citation Section -->
      <div>
        <h2 class="text-2xl font-bold text-slate-900 mb-4">Citation</h2>
        <Card>
          <CardContent class="pt-6">
            <p class="text-slate-600 mb-4">
              If you use MetHMMDB in your research, please cite our work:
            </p>
            <div
              class="bg-slate-50 border border-slate-200 rounded-md p-4 font-mono text-sm text-slate-700"
            >
              Ciuchcinski K, Dziurzynski M. (2025). Fast and accurate detection
              of metal resistance genes using MetHMMDb.
              <em>bioRxiv</em> 2024.12.26.629440
            </div>
            <p class="text-slate-500 mt-4 text-sm">
              The paper is currently under review. In the meantime, you can find
              it on bioRxiv:
              <a
                href="https://doi.org/10.1101/2024.12.26.629440"
                target="_blank"
                rel="noopener noreferrer"
                class="text-blue-600 hover:underline"
                >10.1101/2024.12.26.629440v2</a
              >
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- GitHub Link -->
      <div class="flex justify-center mt-8">
        <Button variant="outline" class="gap-2" asChild>
          <a
            href="https://github.com/Haelmorn/MetHMMDB"
            target="_blank"
            rel="noopener noreferrer"
          >
            <GitBranch class="h-4 w-4" />
            View on GitHub
          </a>
        </Button>

        <Button variant="outline" class="gap-2 ml-4" asChild>
          <a
            href="https://www.biorxiv.org/content/10.1101/2024.12.26.629440v2"
            target="_blank"
            rel="noopener noreferrer"
          >
            <BookOpen class="h-4 w-4" />
            Read the Paper
          </a>
        </Button>
      </div>
    </div>
  </div>
</template>
