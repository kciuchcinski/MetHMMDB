<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  Settings2,
  SortAsc,
  SortDesc,
  Database,
  FileText,
  AlignLeft,
} from "lucide-vue-next";

// --- Reactive State ---
const modelsData = ref<any | null>(null);
const allModels = ref<any[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

const searchTerm = ref("");
const selectedMetalTypes = ref<string[]>([]);
const selectedResistanceType = ref<string | null>(null);
const lengthRange = ref<[number, number]>([0, 10000]);
const sequenceCountRange = ref<[number, number]>([0, 1000]); // New range for sequence count

const viewMode = ref<"table" | "card">("table");
const sortKey = ref<string>("id");
const sortOrder = ref<"asc" | "desc">("asc");

// --- Data for Filters ---
const uniqueMetalTypes = ref<string[]>([]);
const uniqueResistanceTypes = ref<string[]>([]);
const minModelLength = ref(0);
const maxModelLength = ref(1000);
const minSequenceCount = ref(0); // New min for sequence count
const maxSequenceCount = ref(1000); // New max for sequence count

const downloadFile = (filePath: string) => {
  if (!filePath) return;
  
  // GitHub raw content URL format
  const baseUrl = 'https://raw.githubusercontent.com/Haelmorn/MetHMMDB/main/DATA/';
  const url = baseUrl + filePath;
  
  window.open(url, '_blank');
}

// --- Fetch Data ---
onMounted(async () => {
  try {
    const response = await fetch("/browse_models_data.json");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    modelsData.value = data;
    allModels.value = data.models || [];

    // Populate filter options from metadata
    if (data.metadata) {
      uniqueMetalTypes.value = data.metadata.metal_types || [];
      uniqueResistanceTypes.value = data.metadata.resistance_types || [];
    }

    // Determine min/max length for slider/filter
    if (allModels.value.length > 0) {
      const lengths = allModels.value
        .map((m) => m.length)
        .filter((l) => typeof l === "number");
      if (lengths.length > 0) {
        minModelLength.value = Math.min(...lengths);
        maxModelLength.value = Math.max(...lengths);
        lengthRange.value = [minModelLength.value, maxModelLength.value];
      }

      // Determine min/max sequence count for slider/filter
      const seqCounts = allModels.value
        .map((m) => m.sequences_count)
        .filter((c) => typeof c === "number");
      if (seqCounts.length > 0) {
        minSequenceCount.value = Math.min(...seqCounts);
        maxSequenceCount.value = Math.max(...seqCounts);
        sequenceCountRange.value = [
          minSequenceCount.value,
          maxSequenceCount.value,
        ];
      }
    }
  } catch (e: any) {
    error.value = e.message;
    console.error("Failed to load models data:", e);
  } finally {
    isLoading.value = false;
  }
});

// --- Computed Property for Displayed Models (Filtering and Sorting) ---
const displayedModels = computed(() => {
  if (!allModels.value) return [];

  let filtered = [...allModels.value];

  // 1. Filter by Search Term (ID, resistance_type)
  if (searchTerm.value) {
    const lowerSearchTerm = searchTerm.value.toLowerCase();
    filtered = filtered.filter(
      (model) =>
        model.id.toLowerCase().includes(lowerSearchTerm) ||
        (model.resistance_type &&
          model.resistance_type.toLowerCase().includes(lowerSearchTerm))
    );
  }

  // 2. Filter by Metal Types (AND logic - model must have ALL selected metals)
  if (selectedMetalTypes.value.length > 0) {
    filtered = filtered.filter((model) => {
      // Skip models with no metal_type array
      if (!model.metal_type || !Array.isArray(model.metal_type)) return false;

      // Check if ALL selected metals are in this model's metal_type array
      return selectedMetalTypes.value.every((selectedMetal) =>
        model.metal_type.includes(selectedMetal)
      );
    });
  }

  // 3. Filter by Resistance Type
  if (selectedResistanceType.value) {
    filtered = filtered.filter(
      (model) => model.resistance_type === selectedResistanceType.value
    );
  }

  // 4. Filter by Length Range
  filtered = filtered.filter(
    (model) =>
      (model.length === null &&
        lengthRange.value[0] === minModelLength.value &&
        lengthRange.value[1] === maxModelLength.value) ||
      (model.length >= lengthRange.value[0] &&
        model.length <= lengthRange.value[1])
  );

  // 5. Filter by Sequence Count Range
  filtered = filtered.filter(
    (model) =>
      (model.sequences_count === null &&
        sequenceCountRange.value[0] === minSequenceCount.value &&
        sequenceCountRange.value[1] === maxSequenceCount.value) ||
      (model.sequences_count >= sequenceCountRange.value[0] &&
        model.sequences_count <= sequenceCountRange.value[1])
  );

  // 6. Sorting
  if (sortKey.value) {
    filtered.sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];

      // Handle null or undefined for sorting
      if (valA == null) valA = sortOrder.value === "asc" ? Infinity : -Infinity;
      if (valB == null) valB = sortOrder.value === "asc" ? Infinity : -Infinity;

      if (typeof valA === "string" && typeof valB === "string") {
        return sortOrder.value === "asc"
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      }
      return sortOrder.value === "asc" ? valA - valB : valB - valA;
    });
  }

  return filtered;
});

// --- Sorting Function ---
const sortBy = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = key;
    sortOrder.value = "asc";
  }
};

// --- Utility for display ---
const formatArray = (arr: string[] | undefined) =>
  arr && arr.length > 0 ? arr.join(", ") : "N/A";

// Pagination state
const currentPage = ref(1);

// Reset to page 1 when filters change
watch(
  [
    searchTerm,
    selectedMetalTypes,
    selectedResistanceType,
    lengthRange,
    sequenceCountRange,
  ],
  () => {
    currentPage.value = 1;
  }
);

// Computed property for paginated models
const paginatedModels = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return displayedModels.value.slice(start, end);
});

// Computed property for total pages
const totalPages = computed(() => {
  return Math.ceil(displayedModels.value.length / pageSize.value);
});

// Function to change page
const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// Dynamic page size calculation
const pageSize = ref(20); // Default fallback

function calculatePageSize() {
  // Get actual viewport height
  const viewportHeight = window.innerHeight
  
  // Get actual header height by measuring DOM elements
  const navbarHeight = document.querySelector('header')?.offsetHeight || 64
  const filterSectionHeight = document.querySelector('aside')?.offsetHeight || 300
  const controlsHeight = 300 // For pagination, view toggles, etc.
  
  // Different heights for table rows vs cards
  const itemHeight = 50
  
  // Calculate available space more accurately
  const availableHeight = viewportHeight - navbarHeight - controlsHeight
  
  // For table view, we have more vertical space since filters are in a sidebar
  // For card view, we need to account for the filters taking up vertical space on mobile
  const effectiveHeight = window.innerWidth >= 768 ? 
    availableHeight : 
    availableHeight - filterSectionHeight
  
  // Calculate items that can fit
  const itemsPerPage = Math.floor(effectiveHeight / itemHeight)
  
  // Set reasonable min/max bounds
  return Math.max(5, Math.min(itemsPerPage, viewMode.value === 'table' ? 25 : 12))
}

// Update page size when necessary
function updatePageSize() {
  const newPageSize = calculatePageSize()
  if (pageSize.value !== newPageSize) {
    pageSize.value = newPageSize
    // Reset to first page when page size changes to avoid empty pages
    currentPage.value = 1
  }
}

// Call on mount and when relevant factors change
onMounted(() => {
  updatePageSize()
  window.addEventListener('resize', updatePageSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updatePageSize)
})

// Update when view mode changes
watch(viewMode, calculatePageSize)

function getPageNumbers(
  currentPage: number,
  totalPages: number,
  maxVisible: number = 5
): number[] {
  // Calculate center point
  let startPage = Math.max(currentPage - Math.floor(maxVisible / 2), 1);
  let endPage = startPage + maxVisible - 1;

  // Adjust if we're near the end
  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(endPage - maxVisible + 1, 1);
  }

  // Generate array of page numbers
  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  return pages;
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex flex-col md:flex-row gap-6">
      <!-- Sidebar for Filters -->
      <aside
        class="w-full md:w-1/4 space-y-6 p-4 border rounded-lg shadow-sm bg-white"
      >
        <h2 class="text-xl font-semibold flex items-center">
          <Settings2 class="mr-2 h-5 w-5" /> Filters
        </h2>

        <!-- Search Input -->
        <div>
          <Label for="search">Search</Label>
          <Input
            id="search"
            type="text"
            placeholder="Search by ID, resistance type..."
            v-model="searchTerm"
            class="mt-1"
          />
        </div>

        <!-- Metal Type Filter -->
        <div>
          <Label>Metal Type</Label>
          <div
            class="mt-1 space-y-2 max-h-60 overflow-y-auto border p-2 rounded-md"
          >
            <div
              v-for="metal in uniqueMetalTypes"
              :key="metal"
              class="flex items-center"
            >
              <input
                type="checkbox"
                :id="`metal-${metal}`"
                :value="metal"
                v-model="selectedMetalTypes"
                class="form-checkbox"
              />
              <Label :for="`metal-${metal}`" class="ml-2 font-normal">{{
                metal
              }}</Label>
            </div>
          </div>
        </div>

        <!-- Resistance Type Filter -->
        <div>
          <Label for="resistance-type">Resistance Type</Label>
          <Select v-model="selectedResistanceType" class="mt-1">
            <SelectTrigger id="resistance-type">
              <SelectValue placeholder="Select resistance type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem :value="null">All Types</SelectItem>
              <SelectItem
                v-for="resType in uniqueResistanceTypes"
                :key="resType"
                :value="resType"
              >
                {{ resType }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <!-- Length Range Filter -->
        <div>
          <Label>Model Length</Label>
          <div class="mt-2">
            <Slider
              v-model="lengthRange"
              :min="minModelLength"
              :max="maxModelLength"
              :step="1"
              class="mb-4"
            />
            <div class="flex justify-between text-xs text-slate-500 mb-2">
              <span>{{ minModelLength }}</span>
              <span>{{ maxModelLength }}</span>
            </div>
            <div class="flex gap-2 items-center">
              <Input
                type="number"
                v-model.number="lengthRange[0]"
                :min="minModelLength"
                :max="lengthRange[1]"
                class="w-20"
              />
              <span class="text-sm text-slate-500">to</span>
              <Input
                type="number"
                v-model.number="lengthRange[1]"
                :min="lengthRange[0]"
                :max="maxModelLength"
                class="w-20"
              />
            </div>
          </div>
        </div>

        <!-- Sequence Count Range Filter -->
        <div>
          <Label>Sequence Count</Label>
          <div class="mt-2">
            <Slider
              v-model="sequenceCountRange"
              :min="minSequenceCount"
              :max="maxSequenceCount"
              :step="1"
              class="mb-4"
            />
            <div class="flex justify-between text-xs text-slate-500 mb-2">
              <span>{{ minSequenceCount }}</span>
              <span>{{ maxSequenceCount }}</span>
            </div>
            <div class="flex gap-2 items-center">
              <Input
                type="number"
                v-model.number="sequenceCountRange[0]"
                :min="minSequenceCount"
                :max="sequenceCountRange[1]"
                class="w-20"
              />
              <span class="text-sm text-slate-500">to</span>
              <Input
                type="number"
                v-model.number="sequenceCountRange[1]"
                :min="sequenceCountRange[0]"
                :max="maxSequenceCount"
                class="w-20"
              />
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="w-full md:w-3/4">
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-3xl font-bold tracking-tight text-slate-900">
            Browse Models
          </h1>
        </div>

        <div v-if="isLoading" class="text-center py-10">Loading models...</div>
        <div v-if="error" class="text-center py-10 text-red-600">
          Error loading data: {{ error }}
        </div>

        <div v-if="!isLoading && !error">
          <div class="mb-4 text-sm text-slate-600">
            Showing {{ displayedModels.length }} of
            {{ allModels.length }} models.
          </div>

          <!-- Table View -->
          <div v-if="viewMode === 'table'">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead @click="sortBy('id')" class="cursor-pointer">
                    ID
                    <SortAsc
                      v-if="sortKey === 'id' && sortOrder === 'asc'"
                      class="inline h-4 w-4"
                    /><SortDesc
                      v-if="sortKey === 'id' && sortOrder === 'desc'"
                      class="inline h-4 w-4"
                    />
                  </TableHead>
                  <TableHead>Resistance Type</TableHead>
                  <TableHead>Metal(s)</TableHead>
                  <TableHead @click="sortBy('length')" class="cursor-pointer">
                    Length
                    <SortAsc
                      v-if="sortKey === 'length' && sortOrder === 'asc'"
                      class="inline h-4 w-4"
                    /><SortDesc
                      v-if="sortKey === 'length' && sortOrder === 'desc'"
                      class="inline h-4 w-4"
                    />
                  </TableHead>
                  <TableHead
                    @click="sortBy('sequences_count')"
                    class="cursor-pointer"
                  >
                    Seqs
                    <SortAsc
                      v-if="
                        sortKey === 'sequences_count' && sortOrder === 'asc'
                      "
                      class="inline h-4 w-4"
                    /><SortDesc
                      v-if="
                        sortKey === 'sequences_count' && sortOrder === 'desc'
                      "
                      class="inline h-4 w-4"
                    />
                  </TableHead>
                  <TableHead>Downloads</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-if="paginatedModels.length === 0">
                  <TableCell :colspan="6" class="text-center"
                    >No models match your criteria.</TableCell
                  >
                </TableRow>
                <TableRow v-for="model in paginatedModels" :key="model.id">
                  <TableCell class="font-medium">{{ model.id }}</TableCell>
                  <TableCell class="text-xs max-w-xs truncate">{{
                    model.resistance_type
                  }}</TableCell>
                  <TableCell>{{ formatArray(model.metal_type) }}</TableCell>
                  <TableCell>{{ model.length ?? "N/A" }}</TableCell>
                  <TableCell>{{ model.sequences_count ?? "N/A" }}</TableCell>
                  <TableCell>
                    <div class="flex gap-1">
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="downloadFile(model.hmm_file)"
                        title="Download HMM"
                      >
                        <FileText class="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="downloadFile(model.alignment_file)"
                        title="Download Alignment"
                      >
                        <AlignLeft class="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="downloadFile(model.sequence_file)"
                        title="Download Sequences"
                      >
                        <Database class="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <!-- Pagination Controls -->
            <div class="flex justify-center items-center space-x-2 mt-6">
              <Button
                variant="outline"
                size="sm"
                :disabled="currentPage === 1"
                @click="goToPage(1)"
              >
                First
              </Button>
              <Button
                variant="outline"
                size="sm"
                :disabled="currentPage === 1"
                @click="goToPage(currentPage - 1)"
              >
                Previous
              </Button>
              <div class="flex items-center space-x-1">
                <!-- Show first page with ellipsis if not in range -->
                <Button
                  v-if="getPageNumbers(currentPage, totalPages)[0] > 1"
                  size="sm"
                  variant="outline"
                  @click="goToPage(1)"
                  class="w-8 h-8 p-0"
                >
                  1
                </Button>
                <span
                  v-if="getPageNumbers(currentPage, totalPages)[0] > 2"
                  class="mx-1"
                  >...</span
                >

                <!-- Dynamic page numbers -->
                <Button
                  v-for="page in getPageNumbers(currentPage, totalPages)"
                  :key="page"
                  size="sm"
                  :variant="page === currentPage ? 'default' : 'outline'"
                  @click="goToPage(page)"
                  class="w-8 h-8 p-0"
                >
                  {{ page }}
                </Button>

                <!-- Show last page with ellipsis if not in range -->
                <span
                  v-if="
                    getPageNumbers(currentPage, totalPages)[
                      getPageNumbers(currentPage, totalPages).length - 1
                    ] <
                    totalPages - 1
                  "
                  class="mx-1"
                  >...</span
                >
                <Button
                  v-if="
                    getPageNumbers(currentPage, totalPages)[
                      getPageNumbers(currentPage, totalPages).length - 1
                    ] < totalPages
                  "
                  size="sm"
                  variant="outline"
                  @click="goToPage(totalPages)"
                  class="w-8 h-8 p-0"
                >
                  {{ totalPages }}
                </Button>
              </div>

              <Button
                variant="outline"
                size="sm"
                :disabled="currentPage === totalPages"
                @click="goToPage(currentPage + 1)"
              >
                Next
              </Button>
              <Button
                variant="outline"
                size="sm"
                :disabled="currentPage === totalPages"
                @click="goToPage(totalPages)"
              >
                Last
              </Button>
            </div>

            <div class="text-sm text-center text-slate-500 mt-2">
              Showing {{ (currentPage - 1) * pageSize + 1 }}-{{
                Math.min(currentPage * pageSize, displayedModels.length)
              }}
              of {{ displayedModels.length }} models
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
