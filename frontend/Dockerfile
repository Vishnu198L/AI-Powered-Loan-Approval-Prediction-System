FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Streamlit dependencies
RUN pip install --no-cache-dir streamlit requests

# Copy frontend
COPY frontend/ ./frontend/

# Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]