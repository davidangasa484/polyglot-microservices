FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies without version pinning
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    nano \
    wget \
    tree \
    jq \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.10
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Go 1.21
RUN wget https://go.dev/dl/go1.21.13.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.21.13.linux-amd64.tar.gz \
    && rm go1.21.13.linux-amd64.tar.gz

# Set up Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Create workspace directory
WORKDIR /workspace

# Copy the microservices project structure into the container
COPY workspace/ /workspace/

# Install Python dependencies for user-service
WORKDIR /workspace/services/user-service
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Node.js dependencies for order-service
WORKDIR /workspace/services/order-service
RUN npm install --omit=dev

# Build Go service to verify it compiles
WORKDIR /workspace/services/inventory-service
RUN go mod download && go mod verify
RUN go build -o inventory-service .

# Set working directory back to project root
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]