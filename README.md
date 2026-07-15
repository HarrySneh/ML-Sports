🏆 Sports Analytics Pro
https://img.shields.io/badge/python-3.9%252B-blue
https://img.shields.io/badge/Streamlit-1.28%252B-red
https://img.shields.io/badge/license-MIT-green

Sports Analytics Pro is a professional‑grade multi‑sport performance dashboard built with Streamlit.
It combines secure authentication, interactive visualizations, AI‑based performance prediction, live match feeds, and data export – all in one intuitive platform.

https://via.placeholder.com/800x400?text=Sports+Analytics+Pro+Dashboard
(Replace with a screenshot of your app)


✨ Features
🔐 Secure Login – bcrypt hashed passwords, environment‑managed credentials.

📊 Interactive Dashboards – Plotly charts for age distribution, performance by sport, physical analysis (height vs weight).

🤖 AI Performance Predictor – Random Forest classifier trained on age, height, and weight to predict athlete performance (High/Low).

⚽ Live Football Matches – Real‑time match data via Football‑Data.org API (with mock fallback).

🔎 Player Search – Instant search across athlete names.

⚖️ Player Comparison – Side‑by‑side stats and bar chart comparison.

📈 Performance Trends – Time‑series analysis (if your data includes dates).

📥 Data Export – Download filtered data as CSV.

🎨 Custom Styling – ESPN‑inspired dark theme.

🛠️ Tech Stack
Frontend/UI – Streamlit

Data & ML – Pandas, NumPy, Scikit‑learn

Visualization – Plotly

Auth – bcrypt, python‑dotenv / st.secrets

Data Validation – Pydantic

Logging – Loguru

Testing – pytest

Containerization – Docker

CI/CD – GitHub Actions

🚀 Quick Start
Prerequisites
Python 3.9+

pip

(Optional) Docker

Local Setup
Clone the repository

bash
git clone https://github.com/harrysneh/ML-Sports.git
cd ML-Sports
Create and activate a virtual environment

bash
python -m venv venv
source venv/bin/activate     # On Windows: .\venv\Scripts\Activate.ps1
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables
Create a .env file in the project root (copy from .env.example):

ini
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<generated_bcrypt_hash>
DATA_PATH=data/athletes.csv          # optional
LIVE_MATCHES_API_URL=https://api.football-data.org/v4/matches  # optional
API_KEY=your_api_key                 # optional
To generate a bcrypt hash for your password, run:

bash
python -c "import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())"
Run the app

bash
streamlit run app.py
Open http://localhost:8501 in your browser.

Using Docker
bash
docker build -t sports-analytics .
docker run -p 8501:8501 --env-file .env sports-analytics
📊 Data Format
The application expects a CSV with the following columns (case‑sensitive):

Column	Type	Description
Name	string	Athlete name
sport	string	Sport category
Age	integer	Age in years (18–45)
Height	integer	Height in cm (140–250)
Weight	integer	Weight in kg (40–150)
performance_score	float	Score from 0 to 100
Date (optional)	date	For trend analysis (YYYY-MM-DD)
If no CSV is provided, the app automatically generates synthetic data.

🧪 Testing
Run the test suite with:

bash
pytest tests/ --cov=src
☁️ Deployment to Streamlit Cloud
Push your repository to GitHub.

Go to share.streamlit.io and connect your repo.

Set the following secrets in the Streamlit dashboard (Settings → Secrets):

toml
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "your_bcrypt_hash"
DATA_PATH = "data/athletes.csv"    # if present in the repo
LIVE_MATCHES_API_URL = "https://api.football-data.org/v4/matches"
API_KEY = "your_api_key"
Click Deploy.

📁 Project Structure
text
sports-analytics-pro/
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── app.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── auth.py
│   ├── data_loader.py
│   ├── model.py
│   ├── api.py
│   ├── schemas.py
│   ├── utils.py
│   └── logger.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_data_loader.py
├── .github/workflows/
│   └── ci.yml
└── data/
    └── athletes.csv      (optional)
🤝 Contributing
Contributions are welcome!
Please open an issue or submit a pull request.

Fork the repo.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgements
Football‑Data.org for the live match API.

Streamlit for the amazing framework.

Plotly for beautiful interactive charts.

Happy Analyzing! 📊🏆

