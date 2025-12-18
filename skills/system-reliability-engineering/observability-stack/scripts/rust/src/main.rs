//! Example Rust Application with OpenTelemetry
//!
//! Demonstrates OpenTelemetry instrumentation in Rust.

use tracing::info;
use crate::telemetry::init_tracer;

mod telemetry;
mod services;

use services::user_service::UserService;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize OpenTelemetry
    init_tracer(
        "my-service",
        "1.0.0",
        std::env::var("ENV")
            .unwrap_or_else(|_| "development".to_string())
            .as_str(),
    )?;

    info!("Service started");

    // Example usage
    let user_service = UserService;
    let user = user_service.get_user_by_id("123".to_string()).await?;
    
    info!(user_id = %user.id, "User fetched successfully");

    // Your application code here

    Ok(())
}

