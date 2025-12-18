/**
 * Node.js Performance Profiler
 * 
 * CPU profiling for Node.js applications using v8-profiler.
 * 
 * Usage:
 *   node performance-profiler.js
 *   node performance-profiler.js --profile-name my-profile
 */

const profiler = require('v8-profiler-node8');
const fs = require('fs');
const path = require('path');

class PerformanceProfiler {
  constructor() {
    this.activeProfiles = new Map();
  }

  startProfiling(name = 'profile') {
    if (this.activeProfiles.has(name)) {
      console.warn(`Profile ${name} is already running`);
      return;
    }
    profiler.startProfiling(name);
    this.activeProfiles.set(name, Date.now());
    console.log(`Started profiling: ${name}`);
  }

  stopProfiling(name = 'profile') {
    if (!this.activeProfiles.has(name)) {
      console.warn(`Profile ${name} is not running`);
      return null;
    }

    const profile = profiler.stopProfiling(name);
    const data = profile.export();
    profile.delete();
    
    const filename = `${name}-${Date.now()}.cpuprofile`;
    const filepath = path.join(process.cwd(), filename);
    
    fs.writeFileSync(filepath, JSON.stringify(data));
    
    const duration = Date.now() - this.activeProfiles.get(name);
    this.activeProfiles.delete(name);
    
    console.log(`Profile saved to ${filepath} (duration: ${duration}ms)`);
    return filepath;
  }

  async profileFunction(fn, name) {
    this.startProfiling(name);
    try {
      const result = await fn();
      this.stopProfiling(name);
      return result;
    } catch (error) {
      this.stopProfiling(name);
      throw error;
    }
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const profiler = new PerformanceProfiler();
  
  const profileName = args.find(arg => arg.startsWith('--profile-name'))?.split('=')[1] || 'profile';
  const duration = parseInt(args.find(arg => arg.startsWith('--duration'))?.split('=')[1] || '30') * 1000;
  
  console.log(`Starting profile: ${profileName} for ${duration}ms`);
  profiler.startProfiling(profileName);
  
  setTimeout(() => {
    profiler.stopProfiling(profileName);
    process.exit(0);
  }, duration);
}

module.exports = PerformanceProfiler;

