#!/bin/bash

# Move frontend Streamlit app to root as app.py
mv frontend/streamlit_app.py app.py

# Move backend files to backend/ (if not already)
mkdir -p backend
mv backend/main.py backend/
mv backend/llm_utils.py backend/

# Move requirements.txt and runtime.txt to root (if not already)
# (Assuming you already have merged requirements.txt and runtime.txt at root)

# Optional: Move .streamlit config if you have it
if [ -d frontend/.streamlit ]; then
  mv frontend/.streamlit .streamlit
fi

echo "Project restructured for Hugging Face Spaces!"