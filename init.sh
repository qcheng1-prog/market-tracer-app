#!/bin/bash
set -e # Exit immediately if a command fails

# 1. Update system and install Docker + Docker Compose plugin
sudo dnf update -y
sudo dnf install -y docker docker-compose-plugin wget unzip

sudo dnf install -y docker

# 2. Create the CLI plugins directory for all users
sudo mkdir -p /usr/local/lib/docker/cli-plugins

# 3. Download the latest Docker Compose V2 binary directly from GitHub
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo curl -SL https://github.com/docker/buildx/releases/download/v0.17.1/buildx-v0.17.1.linux-amd64 -o /usr/local/lib/docker/cli-plugins/docker-buildx

# 4. Make the binary executable
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

# 5. Add the Docker CLI plugins directory to the PATH    
sudo ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose

# 6. Start and enable Docker engine
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# 7. Prepare target directory and download archive
TARGET_DIR="/web/market-data-tracer-html"
sudo mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

sudo wget http://webpages.charlotte.edu/qcheng1/tbox/cloudi/apps/ec2-docker-market-data-tracker.zip
sudo unzip -o ec2-docker-market-data-tracker.zip -d .
cd "$TARGET_DIR/ec2-docker-market-data-tracker"

# 8. Handle nested folder extraction (if zip extracts into a subfolder)
if [ ! -f "docker-compose.yml" ]; then
    SUBFOLDER=$(find . -maxdepth 2 -name "docker-compose.yml" -exec dirname {} \;)
    if [ -n "$SUBFOLDER" ]; then
        cd "$SUBFOLDER"
    fi
fi

# 9. Launch Docker Compose stack
docker compose up -d