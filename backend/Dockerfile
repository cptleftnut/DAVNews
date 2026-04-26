FROM python:3.11-slim

WORKDIR /app

# System deps for MoviePy / FFmpeg / ImageMagick (TextClip)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        imagemagick \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Allow ImageMagick to handle text rendering for MoviePy
RUN sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@*"/' \
    /etc/ImageMagick-6/policy.xml 2>/dev/null || true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/output

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
