//! User Service with Custom Spans
//!
//! Example service demonstrating custom spans and tracing in Rust.

use opentelemetry::trace::{Span, Status, Tracer};
use opentelemetry::global;
use opentelemetry::KeyValue;
use tracing::{error, instrument};

pub struct UserService;

#[derive(Debug)]
pub struct User {
    pub id: String,
    pub name: String,
    pub email: String,
}

#[derive(Debug)]
pub struct ServiceError {
    pub message: String,
}

impl UserService {
    /// Get user by ID with custom span.
    ///
    /// # Arguments
    ///
    /// * `user_id` - User ID to fetch
    ///
    /// # Returns
    ///
    /// Result containing User or ServiceError
    #[instrument(skip(self), fields(user.id = %user_id))]
    pub async fn get_user_by_id(&self, user_id: String) -> Result<User, ServiceError> {
        let tracer = global::tracer("user-service");
        let mut span = tracer.start("getUserById");
        
        span.set_attribute(KeyValue::new("user.id", user_id.clone()));
        span.set_attribute(KeyValue::new("operation.type", "read"));

        span.add_event("Fetching user from database", vec![]);

        match self.fetch_user_from_db(&user_id).await {
            Ok(user) => {
                span.set_attribute(KeyValue::new("user.found", true));
                span.set_status(Status::Ok);
                span.end();
                Ok(user)
            }
            Err(e) => {
                span.set_status(Status::error(e.message.clone()));
                span.record_exception(&e);
                error!(error = %e.message, "Failed to fetch user");
                span.end();
                Err(e)
            }
        }
    }

    async fn fetch_user_from_db(&self, user_id: &str) -> Result<User, ServiceError> {
        // Simulate database query
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        
        Ok(User {
            id: user_id.to_string(),
            name: "John Doe".to_string(),
            email: "john@example.com".to_string(),
        })
    }
}

