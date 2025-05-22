from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
import os
import pyhmmer
from pyhmmer.plan7 import HMMFile, Pipeline
from pyhmmer.easel import TextSequence, Alphabet
import logging
import json
from functools import lru_cache
from contextlib import contextmanager
import time

# --- Environment Configuration ---
class Config:
    # Use environment variables with defaults
    HMM_DB_PATH = os.getenv("HMM_DB_PATH", "data/methmmdb_v1.0.hmm")
    METADATA_PATH = os.getenv("METADATA_PATH", "data/browse_models_data.json")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEFAULT_EVALUE_THRESHOLD = float(os.getenv("DEFAULT_EVALUE_THRESHOLD", "1e-5"))
    MAX_EVALUE_THRESHOLD = float(os.getenv("MAX_EVALUE_THRESHOLD", "10.0"))
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    NUM_CPUS = int(os.getenv("NUM_CPUS", "4"))

# --- Logging Setup ---
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
class SearchRequest(BaseModel):
    sequence: str = Field(..., description="Protein sequence to search")
    
    @field_validator('sequence')
    def validate_sequence(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Sequence cannot be empty")
        
        valid_chars = set("ACDEFGHIKLMNPQRSTVWYX*")
        invalid_chars = [c.upper() for c in v if c.isalpha() and c.upper() not in valid_chars]
        
        if invalid_chars:
            raise ValueError(f"Invalid amino acid characters found: {', '.join(set(invalid_chars))}")
        return v

class SearchHit(BaseModel):
    model: str
    e_value: float
    score: float
    bias: Optional[float] = None
    metal_type: List[str] = []
    resistance_type: str = ""

class SearchResponse(BaseModel):
    query: str
    hits: List[SearchHit]
    search_params: Dict[str, Any] = {}
    execution_time_ms: int

# --- FastAPI App Setup ---
app = FastAPI(
    title="MetHMMDB Protein Sequence Search API",
    description="API for searching protein sequences against metal resistance HMM databases",
    version="1.0.0",
    redirect_slashes=False,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --- Global Variables ---
hmm_db: List[pyhmmer.plan7.HMM] = []
model_metadata_map: Dict[str, Dict] = {}

# --- Performance Monitoring ---
@contextmanager
def timer():
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)
        logger.debug(f"Operation completed in {elapsed_ms}ms")

# --- Cache for Pipeline Objects ---
@lru_cache(maxsize=8)
def get_pipeline(e_value: float = None) -> Pipeline:
    """Create and cache a Pipeline with the specified E-value threshold."""
    alphabet = Alphabet.amino()
    if e_value is not None:
        return Pipeline(alphabet=alphabet, E=e_value)
    return Pipeline(alphabet=alphabet)

# --- Application Startup ---
@app.on_event("startup")
async def load_resources():
    """Load HMMs and metadata when the application starts."""
    global hmm_db, model_metadata_map
    try:
        # Load HMMs
        with timer():
            with HMMFile(Config.HMM_DB_PATH) as hmm_file_obj:
                hmm_db = list(hmm_file_obj)
            logger.info(f"Successfully loaded {len(hmm_db)} HMMs from {Config.HMM_DB_PATH}")
            if not hmm_db:
                logger.warning(f"HMM database at {Config.HMM_DB_PATH} was loaded but is empty.")

        # Load metadata
        with timer():
            with open(Config.METADATA_PATH, 'r') as f:
                metadata_json = json.load(f)
                for model_entry in metadata_json.get('models', []):
                    model_id = model_entry.get('id')
                    if model_id:
                        model_metadata_map[model_id] = {
                            'metal_type': model_entry.get('metal_type', []),
                            'resistance_type': model_entry.get('resistance_type', "")
                        }
            logger.info(f"Successfully loaded metadata for {len(model_metadata_map)} models from {Config.METADATA_PATH}")

    except FileNotFoundError as e:
        logger.error(f"Required data file not found: {e.filename}. Application startup failed.")
        raise RuntimeError(f"Failed to load critical data file: {e.filename}") from e
    except Exception as e:
        logger.error(f"Error during application startup loading data: {e}", exc_info=True)
        raise RuntimeError(f"An unexpected error occurred during data loading: {e}") from e

# --- Dependency for sequence validation ---
def validate_and_prepare_sequence(request: SearchRequest) -> TextSequence:
    """Validate and prepare a sequence for searching."""
    sequence_str = request.sequence.strip()
    try:
        return TextSequence(name=b"user_query_seq", sequence=sequence_str)
    except Exception as e:
        logger.error(f"Error preparing sequence: {e}")
        raise HTTPException(status_code=400, detail=f"Error preparing sequence: {str(e)}")

# --- API Endpoints ---
@app.post("/search", response_model=SearchResponse)
async def search_sequence_with_pipeline(
    request: SearchRequest,
    evalue: float = Query(
        Config.DEFAULT_EVALUE_THRESHOLD,
        description="E-value threshold for filtering results (lower is more stringent)",
        ge=0.0,
        le=Config.MAX_EVALUE_THRESHOLD
    ),
    text_sequence: TextSequence = Depends(validate_and_prepare_sequence)
):
    """
    Search a protein sequence against the HMM database with optional E-value filtering.
    
    - **sequence**: The protein sequence to search
    - **evalue**: E-value threshold for filtering results (lower is more stringent)
    """
    if not hmm_db:
        logger.error("HMM database is not loaded or empty. Cannot perform search.")
        raise HTTPException(status_code=503, detail="HMM database not available. Please check server logs.")

    logger.info(f"Pipeline Search: Received sequence: {request.sequence[:30]}... with E-value threshold: {evalue}")
    
    with timer() as search_timer:
        try:
            # Prepare the sequence
            alphabet = Alphabet.amino()
            digital_sequence = text_sequence.digitize(alphabet)
            
            # Get the pipeline with the specified E-value threshold
            pipeline = get_pipeline(evalue)
            
            all_search_hits: List[SearchHit] = []
            
            # Process each HMM
            for hmm in hmm_db:
                sequence_block = pyhmmer.easel.DigitalSequenceBlock(alphabet)
                sequence_block.append(digital_sequence)
                hits_for_this_hmm = pipeline.search_hmm(hmm, sequence_block)
                
                if hits_for_this_hmm:
                    hmm_name_decoded = hmm.name.decode()
                    logger.debug(f"HMM '{hmm_name_decoded}' found {len(hits_for_this_hmm)} domain hits.")
                    
                    for hit in hits_for_this_hmm:
                        # Only include hits that pass the E-value threshold
                        if hit.evalue <= evalue:
                            metadata = model_metadata_map.get(hmm_name_decoded, {})
                            
                            all_search_hits.append(SearchHit(
                                model=hmm_name_decoded,
                                e_value=hit.evalue,
                                score=hit.score,
                                bias=hit.bias,
                                metal_type=metadata.get('metal_type', []),
                                resistance_type=metadata.get('resistance_type', "")
                            ))
            
            # Sort all collected hits by E-value (lower is better)
            all_search_hits.sort(key=lambda x: x.e_value)
            
            execution_time = int(search_timer.elapsed_ms if hasattr(search_timer, 'elapsed_ms') else 0)
            logger.info(f"Pipeline Search complete in {execution_time}ms. Found {len(all_search_hits)} hits with E-value <= {evalue}.")
            
            return SearchResponse(
                query=text_sequence.name.decode(),
                hits=all_search_hits,
                search_params={"evalue_threshold": evalue},
                execution_time_ms=execution_time
            )

        except ValueError as ve:
            logger.warning(f"ValueError during sequence processing or search: {ve}")
            raise HTTPException(status_code=400, detail=f"Invalid sequence or search parameter: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during Pipeline HMM search: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error during search.")

# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    if not hmm_db:
        return {"status": "warning", "message": "HMM database not loaded or empty"}
    return {"status": "ok", "hmm_count": len(hmm_db), "metadata_count": len(model_metadata_map)}

# --- Error Handlers ---
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
