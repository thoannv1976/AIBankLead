# BankLead AI - Streamlit app on Google Cloud Run
FROM python:3.11-slim

# Don't write .pyc files; flush logs straight to the Cloud Run console.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System libs needed by xgboost (libgomp) and general builds.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source.
COPY . .

# Generate the bundled sample dataset at build time (optional, harmless).
RUN python sample_data/generate_sample.py || true

# Cloud Run sends traffic to the port named by $PORT (defaults to 8080).
ENV PORT=8080
EXPOSE 8080

# Streamlit must bind 0.0.0.0 and the Cloud Run $PORT. Headless + CORS/XSRF
# off so the container serves cleanly behind the Cloud Run proxy.
CMD streamlit run app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
