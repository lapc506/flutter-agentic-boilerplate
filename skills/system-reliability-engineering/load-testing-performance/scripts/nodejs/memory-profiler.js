/**
 * Node.js Memory Profiler
 * 
 * Memory profiling and monitoring for Node.js applications.
 * 
 * Usage:
 *   node memory-profiler.js
 *   node memory-profiler.js --snapshot
 *   node memory-profiler.js --monitor
 */

const heapdump = require('heapdump');
const path = require('path');

class MemoryProfiler {
  constructor() {
    this.monitoringInterval = null;
  }

  takeSnapshot(filename = null) {
    const timestamp = Date.now();
    const defaultFilename = `heap-${timestamp}.heapsnapshot`;
    const filepath = filename || path.join(process.cwd(), defaultFilename);
    
    heapdump.writeSnapshot(filepath, (err, filename) => {
      if (err) {
        console.error('Error taking heap snapshot:', err);
      } else {
        console.log(`Heap snapshot saved to ${filename}`);
      }
    });
  }

  monitorMemory(intervalMs = 5000) {
    if (this.monitoringInterval) {
      console.log('Memory monitoring already active');
      return;
    }

    console.log(`Starting memory monitoring (interval: ${intervalMs}ms)`);
    
    this.monitoringInterval = setInterval(() => {
      const usage = process.memoryUsage();
      console.log({
        timestamp: new Date().toISOString(),
        rss: `${Math.round(usage.rss / 1024 / 1024)} MB`,
        heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)} MB`,
        heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)} MB`,
        external: `${Math.round(usage.external / 1024 / 1024)} MB`,
        arrayBuffers: `${Math.round(usage.arrayBuffers / 1024 / 1024)} MB`,
      });
    }, intervalMs);
  }

  stopMonitoring() {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
      console.log('Memory monitoring stopped');
    }
  }

  getMemoryUsage() {
    const usage = process.memoryUsage();
    return {
      rss: Math.round(usage.rss / 1024 / 1024),
      heapTotal: Math.round(usage.heapTotal / 1024 / 1024),
      heapUsed: Math.round(usage.heapUsed / 1024 / 1024),
      external: Math.round(usage.external / 1024 / 1024),
      arrayBuffers: Math.round(usage.arrayBuffers / 1024 / 1024),
    };
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const profiler = new MemoryProfiler();
  
  if (args.includes('--snapshot')) {
    const filename = args.find(arg => arg.startsWith('--filename'))?.split('=')[1];
    profiler.takeSnapshot(filename);
  } else if (args.includes('--monitor')) {
    const interval = parseInt(args.find(arg => arg.startsWith('--interval'))?.split('=')[1] || '5000');
    profiler.monitorMemory(interval);
    
    // Keep process alive
    process.on('SIGINT', () => {
      profiler.stopMonitoring();
      process.exit(0);
    });
  } else {
    // Default: show current memory usage
    const usage = profiler.getMemoryUsage();
    console.log('Current memory usage:', usage);
  }
}

module.exports = MemoryProfiler;

