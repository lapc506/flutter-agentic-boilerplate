#!/bin/bash
# Sign Container Image with Notary
#
# Usage:
#   ./sign-image.sh --image gcr.io/my-project/my-app:latest
#   ./sign-image.sh --image my-image:latest --notary-server https://notary-server:4443

set -e

IMAGE=""
NOTARY_SERVER="${NOTARY_SERVER:-https://notary-server:4443}"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --image)
            IMAGE="$2"
            shift 2
            ;;
        --notary-server)
            NOTARY_SERVER="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$IMAGE" ]; then
    echo "❌ Error: --image is required"
    echo "Usage: $0 --image <image> [--notary-server <server>]"
    exit 1
fi

echo "🔐 Signing image: $IMAGE"
echo "   Notary server: $NOTARY_SERVER"
echo ""

# Pull image
echo "📥 Pulling image..."
docker pull "$IMAGE"

# Get image digest
IMAGE_DIGEST=$(docker inspect --format='{{.Id}}' "$IMAGE" | cut -d':' -f2)
echo "   Image digest: $IMAGE_DIGEST"
echo ""

# Sign with Notary
echo "✍️  Signing image with Notary..."
notary -s "$NOTARY_SERVER" \
  -d ~/.docker/trust \
  add \
  "$IMAGE" \
  "$IMAGE_DIGEST"

echo ""
echo "✅ Image signed successfully!"

