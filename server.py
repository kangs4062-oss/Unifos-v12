# server.py - Mock AI generation backend (FastAPI)
# Run: pip install -r requirements.txt
# Start: uvicorn server:app --reload --port 8000

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time, threading, uuid, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

# Copy demo GLB into static (this mock uses the procedural export if present)
SAMPLE_GLB = os.path.join(os.path.dirname(__file__), 'sample_assets', 'ai-wolf-scene.glb')

@app.get('/generate')
def generate():
    """Simulate an AI job that generates a GLB and returns a URL when done."""
    job_id = str(uuid.uuid4())
    # In a real system you'd enqueue a background job. Here we simulate a quick sync op.
    # For demo, we return the sample GLB URL (if exists) otherwise 404.
    if os.path.exists(SAMPLE_GLB):
        return JSONResponse({'status':'done', 'job_id': job_id, 'url': f'/static/{os.path.basename(SAMPLE_GLB)}'})
    else:
        return JSONResponse({'status':'error', 'message':'sample GLB not found on server.'}, status_code=404)

@app.get('/static/{file_name}')
def get_static(file_name: str):
    path = os.path.join(STATIC_DIR, file_name)
    if os.path.exists(path):
        return FileResponse(path, media_type='application/octet-stream')
    return JSONResponse({'error':'not found'}, status_code=404)

if __name__ == '__main__':
    print('Run with: uvicorn server:app --reload --port 8000')
