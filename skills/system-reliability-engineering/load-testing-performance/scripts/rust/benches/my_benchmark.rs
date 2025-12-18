//! Performance benchmarks for API request processing
//!
//! Usage:
//!   cargo bench
//!   cargo bench -- --profile-time=10

use criterion::{black_box, criterion_group, criterion_main, Criterion};

// Example function to benchmark
// Replace with your actual function
fn process_request(data: &str) -> String {
    // Simulate request processing
    format!("processed: {}", data)
}

fn benchmark_requests(c: &mut Criterion) {
    let mut group = c.benchmark_group("api_requests");
    
    // Configure benchmark settings
    group.sample_size(100);
    group.measurement_time(std::time::Duration::from_secs(10));
    
    group.bench_function("process_request", |b| {
        b.iter(|| {
            process_request(black_box("test_data"));
        });
    });
    
    group.bench_function("process_request_large", |b| {
        let large_data = "x".repeat(10000);
        b.iter(|| {
            process_request(black_box(&large_data));
        });
    });
    
    group.finish();
}

criterion_group!(benches, benchmark_requests);
criterion_main!(benches);

