# hackathon-research-park

## Project Setup Instructions

### Backend Setup (FastAPI)

1. **Install [Miniconda/Anaconda](https://docs.conda.io/en/latest/miniconda.html) if you don't have it already.**
2. **Create and activate a new conda environment:**
   ```bash
   conda create -n hackathon-rp python=3.12 -y
   conda activate hackathon-rp
   ```
3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. **Run the FastAPI server:**
   ```bash
   uvicorn src.main:app --reload
   ```
   (Adjust the module path if your main FastAPI app is elsewhere.)

### Frontend Setup (Vite + React)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The app will be available at the local address shown in your terminal (usually http://localhost:5173).

---

For more details on frontend configuration, see `frontend/README.md`.