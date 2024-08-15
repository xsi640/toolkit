docker run --rm -v /root/python:/app \
        -v /root/.pip:/root/.pip \
         -w /app python:3.12.5-alpine \
         pip install --no-cache-dir -r requirements.txt && \
         python xxx.py