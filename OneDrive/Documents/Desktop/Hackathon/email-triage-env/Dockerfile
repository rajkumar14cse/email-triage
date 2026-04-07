FROM --platform=linux/amd64 python:3.11-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user:user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user:user . /app

# Install the package with entry points
RUN pip install --no-cache-dir --user -e .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["server"]