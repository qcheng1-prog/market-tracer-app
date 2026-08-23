#!/bin/bash
set -e # Exit immediately if a command fails

# 1. Update system and install Docker + Docker Compose plugin
dnf update -y
dnf install -y docker docker-compose-plugin wget unzip

# 2. Start and enable Docker engine
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# 3. Prepare target directory and download archive
TARGET_DIR="/var/www/market-data-tracer-html"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

wget http://webpages.charlotte.edu/qcheng1/tbox/cloudi/apps/ec2-docker-market-data-tracker.zip
unzip -o ec2-docker-market-data-tracker.zip -d .

# 4. Handle nested folder extraction (if zip extracts into a subfolder)
if [ ! -f "docker-compose.yml" ]; scheme; then
    SUBFOLDER=$(find . -maxdepth 2 -name "docker-compose.yml" -exec dirname {} \;)
    if [ -n "$SUBFOLDER" ]; then
        cd "$SUBFOLDER"
    fi
fi

# 5. Launch Docker Compose stack
docker compose up -d