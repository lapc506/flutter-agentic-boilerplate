#!/usr/bin/env python3
"""
SLO API Service

FastAPI service for querying SLO compliance and error budget status
from Prometheus metrics.

Usage:
    uvicorn slo_api:app --host 0.0.0.0 --port 8000
    # Or with custom Prometheus URL:
    PROMETHEUS_URL=http://prometheus:9090 uvicorn slo_api:app --reload
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import requests

app = FastAPI(
    title="SLO API Service",
    description="API for querying SLO compliance and error budget status",
    version="1.0.0"
)

# Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
PROMETHEUS_API = f"{PROMETHEUS_URL}/api/v1"


class SLOComplianceResponse(BaseModel):
    """Response model for SLO compliance."""
    service: str
    slo_target: float
    current_availability: float
    is_compliant: bool
    error_budget_remaining: float = Field(..., ge=0, le=1)
    window_days: int
    timestamp: str


class ErrorBudgetResponse(SLOComplianceResponse):
    """Response model for error budget status."""
    burn_rate: float
    days_to_exhaustion: float
    status: str


class SLOService:
    """
    Service for querying SLO compliance from Prometheus.

    This service queries Prometheus metrics to calculate:
    - Current availability
    - SLO compliance status
    - Error budget remaining
    - Burn rate
    - Time to exhaustion
    """

    def __init__(self, prometheus_url: str = PROMETHEUS_URL):
        """
        Initialize SLO Service.

        Args:
            prometheus_url: URL of Prometheus instance
        """
        self.prometheus_url = prometheus_url
        self.api_url = f"{prometheus_url}/api/v1"

    def _query_prometheus(self, query: str, start: datetime, end: datetime, step: str = "1h") -> list:
        """
        Query Prometheus range API.

        Args:
            query: PromQL query
            start: Start time
            end: End time
            step: Query resolution step width

        Returns:
            List of time series values
        """
        params = {
            "query": query,
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": step
        }

        try:
            response = requests.get(f"{self.api_url}/query_range", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data["status"] != "success":
                raise ValueError(f"Prometheus query failed: {data.get('error', 'Unknown error')}")

            result = data["data"]["result"]
            if not result:
                return []

            # Extract values from time series
            values = []
            for series in result:
                values.extend([float(v[1]) for v in series["values"]])

            return values

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to query Prometheus: {str(e)}"
            )

    def _query_prometheus_instant(self, query: str) -> float:
        """
        Query Prometheus instant API.

        Args:
            query: PromQL query

        Returns:
            Single value result
        """
        params = {"query": query}

        try:
            response = requests.get(f"{self.api_url}/query", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data["status"] != "success":
                raise ValueError(f"Prometheus query failed: {data.get('error', 'Unknown error')}")

            result = data["data"]["result"]
            if not result:
                return 0.0

            return float(result[0]["value"][1])

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to query Prometheus: {str(e)}"
            )

    def get_slo_compliance(
        self,
        service: str,
        slo_target: float,
        window_days: int = 30
    ) -> SLOComplianceResponse:
        """
        Get SLO compliance status for a service.

        Args:
            service: Service name
            slo_target: SLO target as decimal (e.g., 0.9995)
            window_days: Evaluation window in days

        Returns:
            SLOComplianceResponse with compliance status
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=window_days)

        # Query availability
        availability_query = f"""
        sum(rate(http_requests_total{{service="{service}", status!~"5.."}}[5m]))[{window_days}d:]
        /
        sum(rate(http_requests_total{{service="{service}"}}[5m]))[{window_days}d:]
        """

        values = self._query_prometheus(availability_query, start_time, end_time, step="1h")

        if not values:
            raise HTTPException(
                status_code=404,
                detail=f"No metrics data available for service '{service}'"
            )

        # Calculate average availability
        avg_availability = sum(values) / len(values) if values else 0.0
        is_compliant = avg_availability >= slo_target

        # Calculate error budget
        error_budget_pct = 1.0 - slo_target
        current_error_rate = 1.0 - avg_availability
        error_budget_remaining = max(0.0, (error_budget_pct - current_error_rate) / error_budget_pct) if error_budget_pct > 0 else 0.0

        return SLOComplianceResponse(
            service=service,
            slo_target=slo_target,
            current_availability=avg_availability,
            is_compliant=is_compliant,
            error_budget_remaining=error_budget_remaining,
            window_days=window_days,
            timestamp=datetime.now().isoformat()
        )

    def get_error_budget_status(
        self,
        service: str,
        slo_target: float,
        window_days: int = 30
    ) -> ErrorBudgetResponse:
        """
        Get detailed error budget status.

        Args:
            service: Service name
            slo_target: SLO target as decimal
            window_days: Evaluation window in days

        Returns:
            ErrorBudgetResponse with detailed budget status
        """
        compliance = self.get_slo_compliance(service, slo_target, window_days)

        # Calculate burn rate (daily consumption rate)
        burn_rate_query = f"""
        (
          sum(rate(http_requests_total{{service="{service}", status=~"5.."}}[5m]))
          /
          sum(rate(http_requests_total{{service="{service}"}}[5m]))
        ) / (1 - {slo_target}) / ({window_days} * 24 * 3600) * 86400
        """

        burn_rate = self._query_prometheus_instant(burn_rate_query)

        # Calculate time to exhaustion
        remaining_budget = compliance.error_budget_remaining
        if burn_rate > 0 and remaining_budget > 0:
            days_to_exhaustion = remaining_budget / burn_rate
        else:
            days_to_exhaustion = float('inf')

        status = self._get_budget_status(compliance.error_budget_remaining, burn_rate)

        return ErrorBudgetResponse(
            **compliance.dict(),
            burn_rate=burn_rate,
            days_to_exhaustion=days_to_exhaustion,
            status=status
        )

    def _get_budget_status(self, remaining: float, burn_rate: float) -> str:
        """
        Get budget status based on remaining budget and burn rate.

        Args:
            remaining: Remaining budget (0-1)
            burn_rate: Daily burn rate (1x = normal)

        Returns:
            Status string
        """
        if remaining <= 0:
            return "exhausted"
        elif remaining < 0.25:
            return "critical"
        elif remaining < 0.5 and burn_rate > 2:
            return "at_risk"
        elif burn_rate > 14:
            return "critical_burn"
        else:
            return "healthy"


# Initialize service
slo_service = SLOService(PROMETHEUS_URL)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "SLO API",
        "version": "1.0.0",
        "endpoints": {
            "compliance": "/slo/{service}/compliance",
            "error_budget": "/slo/{service}/error-budget",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        # Try to query Prometheus
        response = requests.get(f"{PROMETHEUS_API}/query", params={"query": "up"}, timeout=5)
        prometheus_healthy = response.status_code == 200
    except:
        prometheus_healthy = False

    return {
        "status": "healthy" if prometheus_healthy else "degraded",
        "prometheus_connected": prometheus_healthy,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/slo/{service}/compliance", response_model=SLOComplianceResponse)
async def get_compliance(
    service: str,
    slo_target: float = Query(0.9995, ge=0, le=1, description="SLO target as decimal (e.g., 0.9995)"),
    window_days: int = Query(30, ge=1, le=365, description="Evaluation window in days")
):
    """
    Get SLO compliance status for a service.

    Args:
        service: Service name
        slo_target: SLO target (default: 0.9995 = 99.95%%)
        window_days: Evaluation window (default: 30 days)

    Returns:
        SLO compliance status
    """
    return slo_service.get_slo_compliance(service, slo_target, window_days)


@app.get("/slo/{service}/error-budget", response_model=ErrorBudgetResponse)
async def get_error_budget(
    service: str,
    slo_target: float = Query(0.9995, ge=0, le=1, description="SLO target as decimal"),
    window_days: int = Query(30, ge=1, le=365, description="Evaluation window in days")
):
    """
    Get detailed error budget status for a service.

    Args:
        service: Service name
        slo_target: SLO target (default: 0.9995 = 99.95%%)
        window_days: Evaluation window (default: 30 days)

    Returns:
        Detailed error budget status including burn rate and time to exhaustion
    """
    return slo_service.get_error_budget_status(service, slo_target, window_days)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
