<script setup lang="ts">
import { ref, computed } from "vue";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, AlertCircle, Loader2, InfoIcon } from "lucide-vue-next";

//const API_URL = "http://localhost:8000/search";
const API_URL = import.meta.env.VITE_API_URL

// State for the form
const sequenceInput = ref("");
const evalueInput = ref(1e-5)
const isSubmitting = ref(false);
const errorMessage = ref<string | null>(null);
const searchResults = ref<any | null>(null);
const activeTab = ref("input");

// Example sequence
const exampleProteinSequence =
  ">example_protein\nMKTIIALSYIFCLVFADYKDDDKLVPRGSPEFIAVIGQSGSGKSTLLR\nCINLLERPTEGAIFIDGEPIASVTPQRRLSIARQLGIVFQNPALFAH\nSIEENIAMPLKVHKLLERVGLADKLHLYPRQLSGGQQQRVSIARAL\nAMEPKILLLDEPTSALDPEMVGEVLDIMQDLNREGMTMVVVTHDLQ";


// Load example sequence
const loadExample = () => {
  sequenceInput.value = exampleProteinSequence;
};

// Parse and validate protein sequence
const parseSequence = (
  input: string
): { valid: boolean; sequence: string; error?: string } => {
  // Remove empty lines and trim
  const lines = input
    .split("\n")
    .filter((line) => line.trim() !== "")
    .map((line) => line.trim());

  if (lines.length === 0) {
    return { valid: false, sequence: "", error: "Please enter a sequence." };
  }

  let sequence = "";

  // Check if it's in FASTA format (starts with >)
  if (lines[0].startsWith(">")) {
    // Extract sequence from remaining lines
    sequence = lines.slice(1).join("");
  } else {
    // Assume it's a raw sequence
    sequence = lines.join("");
  }

  // Remove any whitespace from sequence
  sequence = sequence.replace(/\s/g, "");

  if (sequence.length === 0) {
    return { valid: false, sequence: "", error: "No sequence content found." };
  }

  // Check if it's a valid protein sequence (contains only amino acid letters)
  // Amino acid letters: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y
  // Also allow X for unknown amino acids and * for stop codons
  const validProteinRegex = /^[ACDEFGHIKLMNPQRSTVWYX*]+$/i;

  if (!validProteinRegex.test(sequence)) {
    return {
      valid: false,
      sequence,
      error:
        "Invalid protein sequence. Protein sequences should only contain amino acid letters (A-Z).",
    };
  }

  return { valid: true, sequence };
};

const submitSequence = async () => {
  // Reset state
  errorMessage.value = null;
  searchResults.value = null;

  // Parse and validate the input
  const { valid, sequence, error } = parseSequence(sequenceInput.value);

  if (!valid) {
    errorMessage.value = error || "Invalid sequence";
    return;
  }

  isSubmitting.value = true;
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sequence: sequence, evalue: evalueInput.value }),
    });

    if (!response.ok) {
      const err = await response.json();
      errorMessage.value = err.detail || "Search failed";
      return;
    }

    const data = await response.json();
    searchResults.value = data;
    activeTab.value = "results";
  } catch (error) {
    errorMessage.value = "Could not connect to backend.";
  } finally {
    isSubmitting.value = false;
  }
};

// Format E-value for display
const formatEValue = (eValue: string) => {
  const num = parseFloat(eValue);
  if (num < 0.0001) {
    return eValue; // Scientific notation
  }
  return num.toFixed(6);
};

// Calculate sequence stats
const sequenceStats = computed(() => {
  const { valid, sequence } = parseSequence(sequenceInput.value);
  if (!valid || !sequence) {
    return { length: 0, valid: false };
  }
  return {
    length: sequence.length,
    valid: true,
  };
});
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-2">Protein Sequence Search</h1>
    <p class="text-slate-600 mb-6">
      Search your protein sequence against MetHMMDB to identify potential metal
      resistance genes.
    </p>

    <!-- Add this alert at the top of the page -->
    <Alert class="mb-6 bg-amber-50 border-amber-200">
      <InfoIcon class="h-4 w-4 text-amber-600" />
      <AlertTitle class="text-amber-800">Note</AlertTitle>
      <AlertDescription class="text-amber-700">
        This is a demonstration version of the search functionality. The search
        feature is working, but the results are not stored, so any work done here will be lost on refresh.
      </AlertDescription>
    </Alert>

    <Tabs v-model="activeTab" class="w-full">
      <TabsList>
        <TabsTrigger value="input">Input Sequence</TabsTrigger>
        <TabsTrigger value="results" :disabled="!searchResults"
          >Results</TabsTrigger
        >
      </TabsList>

      <TabsContent value="input" class="space-y-4">
        <div class="flex gap-2 mb-2">
          <Button variant="outline" size="sm" @click="loadExample">
            Load Example Protein
          </Button>
        </div>

        <div>
          <label
            for="sequence"
            class="block text-sm font-medium text-slate-700 mb-1"
          >
            Enter your protein sequence (FASTA format or raw sequence):
          </label>
          <Textarea
            id="sequence"
            v-model="sequenceInput"
            rows="12"
            class="font-mono text-sm"
            placeholder=">sequence_name
MKTIIALSYIFCLVFADYKDDDK"
            required
          ></Textarea>
          <div class="flex justify-between text-xs text-slate-500 mt-1">
            <p>
              Accepts protein sequences only. FASTA format is preferred but not
              required.
            </p>
            <p v-if="sequenceInput.trim()">
              Sequence length: {{ sequenceStats.length }} amino acids
              <span v-if="!sequenceStats.valid" class="text-red-500">
                (invalid format)</span
              >
            </p>
          </div>
        </div>
        <div>
          <label
            for="evalue"
            class="block text-sm font-medium text-slate-700 mb-1"
          >
            E-value threshold:
          </label>
          <input
            id="evalue"
            type="number"
            v-model.number="evalueInput"
            class="border border-slate-300 rounded-md p-2 w-full"
            min="0"
            step="0.0001"
          />
          <p class="text-xs text-slate-500 mt-1">
            Default: 1e-5. Lower values yield more stringent results.
            Both text (e.g., 1e-5) and decimal (e.g., 0.00001) formats are accepted.
          </p>
        </div>

        <div v-if="errorMessage" class="mt-4">
          <Alert variant="destructive">
            <AlertCircle class="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{{ errorMessage }}</AlertDescription>
          </Alert>
        </div>

        <div class="flex justify-end mt-4">
          <Button
            type="submit"
            @click="submitSequence"
            :disabled="
              isSubmitting || !sequenceInput.trim() || !sequenceStats.valid
            "
          >
            <Loader2 v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin" />
            <Search v-else class="mr-2 h-4 w-4" />
            {{ isSubmitting ? "Searching..." : "Search Database" }}
          </Button>
        </div>
      </TabsContent>

      <TabsContent value="results">
        <div v-if="searchResults" class="space-y-6">
          <div>
            <h2 class="text-xl font-semibold mb-2">Search Results</h2>
            <p class="text-slate-600">
              Query: <span class="font-mono">{{ searchResults.query }}</span>
            </p>
            <p class="text-slate-600">
              Sequence length: {{ sequenceStats.length }} amino acids
            </p>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full border-collapse">
              <thead>
                <tr class="bg-slate-100">
                  <th class="border px-4 py-2 text-left">Model</th>
                  <th class="border px-4 py-2 text-left">E-value</th>
                  <th class="border px-4 py-2 text-left">Score</th>
                  <th class="border px-4 py-2 text-left">Metal Type</th>
                  <th class="border px-4 py-2 text-left">Resistance Type</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(hit, index) in searchResults.hits"
                  :key="index"
                  class="hover:bg-slate-50"
                >
                  <td class="border px-4 py-2 font-medium">{{ hit.model }}</td>
                  <td class="border px-4 py-2 font-mono">
                    {{ formatEValue(hit.e_value) }}
                  </td>
                  <td class="border px-4 py-2">{{ hit.score.toFixed(1) }}</td>
                  <td class="border px-4 py-2">
                    {{ hit.metal_type.join(", ") }}
                  </td>
                  <td class="border px-4 py-2">{{ hit.resistance_type }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="flex justify-between">
            <Button variant="outline" @click="activeTab = 'input'">
              New Search
            </Button>
            <Button variant="outline"> Download Results </Button>
          </div>
        </div>
      </TabsContent>
    </Tabs>
  </div>
</template>
