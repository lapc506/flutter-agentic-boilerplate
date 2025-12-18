#!/bin/bash
# Install Istio Service Mesh
#
# Usage:
#   ./install-istio.sh
#   ./install-istio.sh --profile demo
#   ./install-istio.sh --version 1.19.0

set -e

ISTIO_VERSION="${ISTIO_VERSION:-latest}"
PROFILE="${PROFILE:-demo}"

echo "🚀 Installing Istio Service Mesh"
echo "   Version: ${ISTIO_VERSION}"
echo "   Profile: ${PROFILE}"
echo ""

# Download Istio
if [ ! -d "istio-${ISTIO_VERSION}" ]; then
    echo "📥 Downloading Istio..."
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -
fi

cd istio-${ISTIO_VERSION}
export PATH=$PWD/bin:$PATH

# Install Istio
echo "📦 Installing Istio with profile: ${PROFILE}"
istioctl install --set profile=${PROFILE} -y

# Verify installation
echo ""
echo "🔍 Verifying installation..."
kubectl get pods -n istio-system

echo ""
echo "✅ Istio installed successfully!"
echo ""
echo "Next steps:"
echo "  1. Label namespace for injection: kubectl label namespace <namespace> istio-injection=enabled"
echo "  2. Deploy your application"
echo "  3. Verify sidecars: kubectl get pods -n <namespace>"

