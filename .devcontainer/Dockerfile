FROM mcr.microsoft.com/devcontainers/python:3.12

# Remove stale yarn repo (has expired GPG key in base image) and install curl
RUN rm -f /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y curl

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

# Install Postman CLI (for API governance validation)
# Using || true to make this optional - container will still build if Postman CLI fails
RUN curl -fsSL 'https://dl-cli.pstmn.io/install/linux64.sh' | sh || echo "Warning: Postman CLI installation failed, continuing without it"

WORKDIR /workspace

ENTRYPOINT ["sleep", "infinity"]
