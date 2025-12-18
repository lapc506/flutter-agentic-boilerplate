#!/bin/bash
# Verify Istio Installation
#
# Usage:
#   ./verify-istio.sh

set -e

echo "🔍 Verifying Istio Installation"
echo ""

# Check Istio namespace
echo "📋 Checking istio-system namespace..."
if kubectl get namespace istio-system &>/dev/null; then
    echo "✅ istio-system namespace exists"
else
    echo "❌ istio-system namespace not found"
    exit 1
fi

# Check Istio pods
echo ""
echo "📦 Checking Istio pods..."
PODS=$(kubectl get pods -n istio-system --no-headers 2>/dev/null | wc -l)
if [ "$PODS" -gt 0 ]; then
    echo "✅ Found ${PODS} pod(s) in istio-system"
    kubectl get pods -n istio-system
else
    echo "❌ No pods found in istio-system"
    exit 1
fi

# Check all pods are running
echo ""
echo "🔍 Checking pod status..."
NOT_READY=$(kubectl get pods -n istio-system --no-headers 2>/dev/null | grep -v Running | grep -v Completed | wc -l)
if [ "$NOT_READY" -eq 0 ]; then
    echo "✅ All pods are running"
else
    echo "⚠️  Some pods are not ready:"
    kubectl get pods -n istio-system | grep -v Running | grep -v Completed
fi

# Check Istio version
echo ""
echo "📊 Istio version:"
istioctl version 2>/dev/null || echo "⚠️  istioctl not found in PATH"

echo ""
echo "✅ Verification complete!"

