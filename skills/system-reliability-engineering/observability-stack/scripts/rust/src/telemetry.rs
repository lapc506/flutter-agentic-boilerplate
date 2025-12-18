//! OpenTelemetry Telemetry Setup for Rust
//!
//! Initialize OpenTelemetry tracing and metrics for Rust applications.
//!
//! Usage:
//!     use crate::telemetry::init_tracer;
//!     
//!     init_tracer("my-service", "1.0.0", "production")?;

use opentelemetry::global;
use opentelemetry::sdk::trace::TracerProvider;
use opentelemetry::sdk::Resource;
use opentelemetry::KeyValue;
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_semantic_conventions::resource::{
    DEPLOYMENT_ENVIRONMENT, SERVICE_NAME, SERVICE_VERSION,
};
use tracing_subscriber::layer::SubscriberExt;
use tracing_subscriber::util::SubscriberInitExt;
use tracing_subscriber::Registry;

/// Initialize OpenTelemetry tracer.
///
/// # Arguments
///
/// * `service_name` - Name of the service
/// * `service_version` - Version of the service
/// * `environment` - Deployment environment (development, staging, production)
///
/// # Returns
///
/// Result indicating success or failure
pub fn init_tracer(
    service_name: &str,
    service_version: &str,
    environment: &str,
) -> Result<(), Box<dyn std::error::Error>> {
    let otlp_endpoint = std::env::var("OTEL_EXPORTER_OTLP_ENDPOINT")
        .unwrap_or_else(|_| "http://localhost:4318/v1/traces".to_string());

    let otlp_exporter = opentelemetry_otlp::new_exporter()
        .http()
        .with_endpoint(otlp_endpoint);

    let tracer_provider = TracerProvider::builder()
        .with_batch_exporter(otlp_exporter)
        .with_resource(Resource::new(vec![
            KeyValue::new(SERVICE_NAME, service_name.to_string()),
            KeyValue::new(SERVICE_VERSION, service_version.to_string()),
            KeyValue::new(DEPLOYMENT_ENVIRONMENT, environment.to_string()),
        ]))
        .build();

    global::set_tracer_provider(tracer_provider);

    // Initialize tracing subscriber
    let telemetry = tracing_opentelemetry::layer()
        .with_tracer(global::tracer("my-service"));

    let subscriber = Registry::default()
        .with(telemetry)
        .with(
            tracing_subscriber::fmt::layer()
                .json()
                .with_target(false)
                .with_current_span(false),
        )
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        );

    subscriber.init();

    Ok(())
}

/// Shutdown OpenTelemetry tracer provider.
pub fn shutdown() {
    global::shutdown_tracer_provider();
}

