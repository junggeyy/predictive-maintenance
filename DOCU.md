# Predictive Maintenance System Documentation

## 0. Prerequisites

This project requires two separate Python virtual environments due to different Python version requirements:

1. Backend & Frontend Environment (Python 3.9)

2. MCP Server Environment (Python 3.10+)

After activation, make sure to install the respective modules from requirements.txt in each of the server files (apps/backend and apps/mcp_server)

**Note:** Make sure to activate the appropriate environment before running each component.


## 1. Running Instructions

### Backend (FastAPI)

Start the FastAPI backend server:

```bash
cd apps/backend
uvicorn src.main:app --reload
```

The backend will be available at `http://localhost:8000`

- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/check`

### Frontend (Streamlit)

Start the Streamlit dashboard:

```bash
cd apps/frontend
streamlit run app.py
```

The frontend will open automatically in your browser at `http://localhost:8501`

#### Running Simulation

On the dashboard, click "Start Simulation" button. 
The simulation will:
- Process 100 machine records
- Run failure classification predictions
- Run RUL (Remaining Useful Life) regression for failing machines
- Store results in-memory for MCP server access

### MCP Server

The MCP server allows LLMs (like Claude, GPT) to query machine status in natural language.

**Start the MCP Server:**

```bash
cd apps/mcp_server
python server.py
```

You should see: `MCP server is listening...`<br>
Then, connect the MCP with the LLM of your choice and you can start using the tool.<br>
**Usage Examples:**
- "What is the status of machine 42?"
- "Is machine 15 healthy?"
- "Which machines need immediate maintenance?"

---

## 2. Directory Structure

```
predictive-analysis/
│
├── apps/                           # Application layer
│   │
│   ├── backend/                    # FastAPI backend server
│   │   ├── src/
│   │   │   ├── core/               # Core utilities (config, loaders)
│   │   │   ├── routers/            # API route definitions
│   │   │   │   └── endpoints/      # API endpoints (predict, mcp, simulation)
│   │   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   ├── services/           # Business logic services
│   │   │   └── main.py             # FastAPI application entry point
│   │   └── requirements.txt        # Backend Python dependencies
│   │
│   ├── frontend/                   
│   │   └── app.py                  # Streamlit UI application
│   │
│   └── mcp_server/                 # Model Context Protocol server
│       ├── server.py               # server implementation
│       ├── tools.py                # tool functions
│       ├── requirements.txt        # MCP server dependencies
│       └── mcp_config_example.json # Example Claude Desktop configuration
│
├── data/                           # Data storage
│   │
│   ├── raw/                        # Original CSV files from Kaggle
│   │
│   ├── processed/                  # Processed datasets and metadata
│   │   ├── classification/         # Classification model metadata
│   │   └── regression/             # Regression model metadata
│   │
│   └── production/                 # Production/test datasets
│
├── models/                         # Trained ML models
│                                   # (classification, regression, scalers)
│
├── notebooks/                      # Jupyter notebooks for development
│                                   # (data exploration, preprocessing, feature engineering,
│                                   #  model training for classification and regression)
│
├── mcp_venv/                       # Python virtual environment for MCP server (Python 3.10+)
├── .venv/                          # Python virtual environment for server & frontend
├── DOCU.md                         # documentation file
└── README.md                       # Project overview
```

