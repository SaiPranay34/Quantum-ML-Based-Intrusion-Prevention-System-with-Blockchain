# Quantum ML-Based Intrusion Prevention System

A proof-of-concept intrusion detection dashboard that combines classical and quantum-feature machine-learning preprocessing with a Flask API, a React dashboard, and an optional Ethereum-compatible ledger for recording detected attacks.

## Features

- User registration and login
- Live detection simulation using the bundled sample datasets
- CSV upload analysis, detection history, statistics, and report downloads
- Visualizations for intrusion activity and model metrics
- Optional blockchain logging of detections through a Solidity contract on Ganache
- Controls for blocked IP addresses and SMTP alert settings

## Project Structure

- `app.py`, `routes/`, `services/`: Flask backend and API
- `frontend/`: React 18 and Vite web client
- `blockchain/`: Web3 integration and Solidity contract
- `datasets/simulation/`, `datasets/upload/`: simulation and example CSV data
- `*_model.pkl`, `scaler_standard.pkl`, `pca_quantum_reducer.pkl`, `quantum_feature_transformer.pkl`: model and preprocessing artifacts loaded by the backend

## Requirements

- Python 3.10 or newer
- Node.js 20 or newer and npm
- Ganache, if using blockchain logging

The model artifact files listed above must be present in the project root. They are included with this project. A working Ganache instance is needed for contract deployment and ledger operations; it should listen at `http://127.0.0.1:7545`.

## Setup and Run

Run the backend and frontend in separate terminals from the project root.

### 1. Install Python dependencies

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. (Optional) Start Ganache and deploy the contract

Start Ganache with its JSON-RPC server on `127.0.0.1:7545`, then from the project root run:

```bash
python deploy.py
```

Deployment updates `config.py` with the newly deployed contract address and ABI. If you skip blockchain setup, the application can still be used for model-backed detection, but ledger functions will be unavailable.

### 3. Start the Flask backend

From the project root, with the virtual environment active:

```bash
python app.py
```

The backend listens on `http://localhost:5000`.

### 4. Start the React frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal (normally `http://localhost:5173`). The Vite development server proxies API requests to the Flask backend.

## CSV Input

Uploaded and simulation CSV files should contain the 45 network traffic feature columns expected by the model. The feature names and order are defined in `services/ml_service.py`. A `label` column may be present in sample datasets; it is not part of the model input.

## Notes

- `python dataset.py` regenerates the simulation and upload example datasets.
- `python verify.py` runs the repository's verification script.
- `python app.py` starts Flask with debug mode enabled; use an appropriate production WSGI server and deployment configuration outside local development.
