#!/bin/bash
# Email Triage System - Deployment Helper Script

set -e

echo "🚀 Email Triage System - Deployment Setup"
echo "==========================================="

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Download: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

echo "✅ Docker Compose found: $(docker-compose --version)"

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# Email Triage Environment Variables
HF_TOKEN=your_huggingface_token_here
API_BASE_URL=https://router.huggingface.co/openai/v1
MODEL_NAME=google/flan-t5-large
ENV_URL=http://localhost:8000
PORT=8000
EOF
    echo "📝 Created .env file. Please edit it with your HF_TOKEN"
fi

# Ask for deployment option
echo ""
echo "Select deployment option:"
echo "1. Run locally with Docker Compose (default)"
echo "2. Build Docker image only"
echo "3. Push to Docker Hub (requires login)"
echo "4. Push to GitHub Container Registry"
echo ""
read -p "Enter choice (1-4, or press Enter for 1): " choice
choice=${choice:-1}

case $choice in
    1)
        echo "🐳 Starting Docker Compose..."
        docker-compose up -d
        echo ""
        echo "✅ Deployment complete!"
        echo "📍 API available at: http://localhost:8000"
        echo "📚 API Docs at: http://localhost:8000/docs"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop: docker-compose down"
        ;;
    2)
        echo "🔨 Building Docker image..."
        docker build -t email-triage:latest .
        echo "✅ Build complete!"
        echo "Run with: docker run -p 8000:8000 email-triage:latest"
        ;;
    3)
        echo "🏪 Pushing to Docker Hub..."
        read -p "Enter your Docker Hub username: " dockerhub_user
        docker build -t $dockerhub_user/email-triage:latest .
        docker push $dockerhub_user/email-triage:latest
        echo "✅ Pushed to Docker Hub: docker.io/$dockerhub_user/email-triage:latest"
        ;;
    4)
        echo "📦 Pushing to GitHub Container Registry..."
        read -p "Enter your GitHub username: " github_user
        read -p "Enter your GitHub token (with read:packages, write:packages): " github_token
        
        echo $github_token | docker login ghcr.io -u $github_user --password-stdin
        docker build -t ghcr.io/$github_user/email-triage:latest .
        docker push ghcr.io/$github_user/email-triage:latest
        echo "✅ Pushed to GitHub Container Registry"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📖 For more deployment options, see DEPLOYMENT.md"
