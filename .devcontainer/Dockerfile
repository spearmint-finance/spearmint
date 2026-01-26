FROM mcr.microsoft.com/devcontainers/python:3.12

# Install Node.js 22 directly (NOT via features - they fail with exit code 100)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install additional tools
RUN apt-get update && apt-get install -y \
    awscli \
    bubblewrap \
    gh \
    htop \
    jq \
    ncdu \
    socat \
    sqlite3 \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for Docker-outside-of-Docker via socket mount)
RUN curl -fsSL https://get.docker.com | sh

WORKDIR /workspace

ENTRYPOINT ["sleep", "infinity"]
