# Setup Instructions (Ubuntu)

Follow these steps to set up and run your Quantum IDS Dashboard on an Ubuntu system. 

## 1. Install System Dependencies

Open your terminal and install the required system packages, including Python and Node.js.

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv curl

# Install Node.js (via NodeSource for a recent version)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. Set Up the Python Backend

Navigate to your project folder (`blockchain`), create a virtual environment, and install the required ML and Flask libraries.

```bash
cd /path/to/your/blockchain

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

Ensure your ML files ([scaler_base.pkl](file:///c:/Users/vedth/OneDrive/Documents/blockchain/scaler_base.pkl), [pca_model.pkl](file:///c:/Users/vedth/OneDrive/Documents/blockchain/pca_model.pkl), [scaler_angle.pkl](file:///c:/Users/vedth/OneDrive/Documents/blockchain/scaler_angle.pkl), [qml_model_weights.pth](file:///c:/Users/vedth/OneDrive/Documents/blockchain/qml_model_weights.pth)) are in the same folder as [app.py](file:///c:/Users/vedth/OneDrive/Documents/blockchain/app.py).

## 3. Set Up the React Frontend

Navigate to the `frontend` folder and install the Node modules.

```bash
cd frontend

# Install package dependencies
npm install
```

## 4. Run the Application

You'll need two terminal windows to run both the backend and frontend simultaneously.

**Terminal 1 (Backend):**
```bash
cd /path/to/your/blockchain
source venv/bin/activate
python3 app.py
```
*The Flask server will start on `http://localhost:5000`.*

**Terminal 2 (Frontend):**
```bash
cd /path/to/your/blockchain/frontend
npm run dev
```
*The Vite development server will start on `http://localhost:5173`. Open this URL in your browser to view the application.*
