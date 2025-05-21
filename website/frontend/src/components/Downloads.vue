<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Download, 
  Database, 
  AlignLeft, 
  FileText, 
  Info, 
  ExternalLink 
} from 'lucide-vue-next'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

// Base URL for GitHub releases
const GITHUB_RELEASE_URL = 'https://github.com/Haelmorn/MetHMMDB/releases/download/v1.0/'

// Function to handle downloads
const downloadFile = (filename: string) => {
  const url = GITHUB_RELEASE_URL + filename
  window.open(url, '_blank')
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="space-y-6">
      <!-- Page Header -->
      <div class="space-y-2">
        <h1 class="text-3xl font-bold tracking-tight text-slate-900">Download MetHMMDB</h1>
        <p class="text-slate-600">Access the complete database or specific subsets for your research needs.</p>
      </div>

      <!-- Main Content -->
      <Tabs defaultValue="all" class="w-full">
        <TabsList class="grid w-full grid-cols-5">
          <TabsTrigger value="all">Complete DB</TabsTrigger>
          <TabsTrigger value="hmms">HMMs</TabsTrigger>
          <TabsTrigger value="alignments">Alignments</TabsTrigger>
          <TabsTrigger value="sequences">Sequences</TabsTrigger>
          <TabsTrigger value="metadata">Metadata</TabsTrigger>
        </TabsList>
        
        <!-- Complete Database Tab -->
        <TabsContent value="all" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <Database class="h-5 w-5" />
                Complete MetHMMDB
              </CardTitle>
              <CardDescription>
                Download the entire database including all HMMs, alignments, sequences, and metadata.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-slate-600 mb-4">
                The complete package contains all 254 profile Hidden Markov Models, multiple sequence alignments, 
                representative protein sequences, and comprehensive metadata for all 121 microbial MMRGs.
              </p>
              <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                <div class="flex items-center gap-2">
                  <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmm_db_v1.0.tar.gz</span>
                </div>
                <Button size="sm" @click="downloadFile('methmm_db_v1.0.tar.gz')">
                  <Download class="mr-2 h-4 w-4" />
                  Download
                </Button>
              </div>
            </CardContent>
            <CardFooter>
              <p class="text-xs text-slate-500">
                Last updated: January 2025 • Version 1.0
              </p>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <!-- HMMs Tab -->
        <TabsContent value="hmms" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <FileText class="h-5 w-5" />
                Profile Hidden Markov Models
              </CardTitle>
              <CardDescription>
                Download the HMMs for sequence searching and annotation.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-slate-600 mb-4">
                This package contains all 254 profile HMMs in HMMER3 format, ready to use with the HMMER software suite
                for sensitive sequence homology searches.
              </p>
              <div class="space-y-3">
                <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmmdb_v1.0.hmm</span>
                  </div>
                  <Button size="sm" @click="downloadFile('methmmdb_v1.0.hmm')">
                    <Download class="mr-2 h-4 w-4" />
                    Download
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <!-- Alignments Tab -->
        <TabsContent value="alignments" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <AlignLeft class="h-5 w-5" />
                Multiple Sequence Alignments
              </CardTitle>
              <CardDescription>
                Download the curated multiple sequence alignments used to build the HMMs.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-slate-600 mb-4">
                This package contains all multiple sequence alignments in fasta format, representing the 
                sequence diversity captured in each HMM profile.
              </p>
              <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                <div class="flex items-center gap-2">
                  <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmm_alignments_v1.0.tar.gz</span>
                </div>
                <Button size="sm" @click="downloadFile('methmm_alignments_v1.0.tar.gz')">
                  <Download class="mr-2 h-4 w-4" />
                  Download
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <!-- Sequences Tab -->
        <TabsContent value="sequences" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <FileText class="h-5 w-5" />
                Protein Sequences
              </CardTitle>
              <CardDescription>
                Download representative protein sequences for each MMRG family.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-slate-600 mb-4">
                This package contains FASTA files with protein sequences used to generate alignments and HMMs, which can be used as a database for sequence-based tools (i.e. MMseqs, DIAMOND, BLAST)
              </p>
              <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                <div class="flex items-center gap-2">
                  <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmm_sequences_v1.0.tar.gz</span>
                </div>
                <Button size="sm" @click="downloadFile('methmm_sequences_v1.0.tar.gz')">
                  <Download class="mr-2 h-4 w-4" />
                  Download
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <!-- Metadata Tab -->
        <TabsContent value="metadata" class="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <Info class="h-5 w-5" />
                Metadata
              </CardTitle>
              <CardDescription>
                Download annotation and classification metadata for all models.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-slate-600 mb-4">
                This package contains metadata in JSON and CSV formats, including functional annotations and cross-references to other databases.
              </p>
              <div class="space-y-3">
                <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmm_metadata_v1.0.json</span>
                  </div>
                  <Button size="sm" @click="downloadFile('methmm_metadata_v1.0.json')">
                    <Download class="mr-2 h-4 w-4" />
                    Download
                  </Button>
                </div>
                <div class="flex items-center justify-between rounded-md border p-3 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="font-mono bg-slate-100 px-2 py-1 rounded text-slate-700">methmm_metadata_v1.0.tsv</span>
                  </div>
                  <Button size="sm" @click="downloadFile('methmm_metadata_v1.0.tsv')">
                    <Download class="mr-2 h-4 w-4" />
                    Download
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <!-- Usage Information -->
      <Card class="bg-slate-50 border-slate-200">
        <CardHeader>
          <CardTitle class="text-lg">How to Use These Files</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4 text-sm text-slate-700">
            <p>
              <strong>HMM Files:</strong> Use with HMMER3 software for sequence searching. Example command:
              <code class="bg-slate-100 px-2 py-1 rounded font-mono">hmmsearch --cpu 8 -E 1e-5 methmmdb_v1.0.hmm your_sequences.fasta</code>
            </p>
            <p>
              <strong>Alignments:</strong> Can be viewed with alignment viewers like Jalview or used to build custom HMMs.
            </p>
            <p>
              <strong>Sequences:</strong> Protein sequences can be used as queries for BLAST-like searches or for phylogenetic analysis.
            </p>
            <p>
              <strong>Metadata:</strong> Contains annotations and classifications that can be integrated into your analysis pipeline.
            </p>
            <p>
              For more detailed instructions, please refer to our 
              <a href="https://github.com/Haelmorn/MetHMMDB#readme" class="text-slate-900 hover:underline" target="_blank" rel="noopener noreferrer">
                documentation <ExternalLink class="inline h-3 w-3" />
              </a>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
