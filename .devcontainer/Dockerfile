FROM mcr.microsoft.com/devcontainers/python:3.12

# Install Node.js 22 (required for Auggie CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install additional tools
RUN apt-get update && apt-get install -y \
    bubblewrap \
    gh \
    htop \
    jq \
    ncdu \
    socat \
    sqlite3 \
    tree \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["sleep", "infinity"]
