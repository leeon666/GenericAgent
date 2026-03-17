@echo off
cd /d "%~dp0"
echo Starting Streamlit with performance optimizations...
python -m streamlit run stapp.py --server.port=8504 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
