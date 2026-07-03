FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('omw-1.4')"

# Copy the backend code
COPY backend/ /app/

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV FLASK_DEBUG=false

# Start the app with gunicorn
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:7860", "--timeout", "120", "--workers", "1"]
