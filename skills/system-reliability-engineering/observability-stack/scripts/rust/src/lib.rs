//! Observability Rust Library
//!
//! OpenTelemetry instrumentation library for Rust applications.

pub mod telemetry;

#[cfg(feature = "services")]
pub mod services;

pub use telemetry::{init_tracer, shutdown};

