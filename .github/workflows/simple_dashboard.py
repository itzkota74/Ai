#!/usr/bin/env python3
# 📊 SIMPLE REAL-TIME DASHBOARD
import json
import time
import os
import subprocess
from datetime import datetime

class SimpleDashboard:
    def __init__(self):
        self.systems = {
            'business': {
                'process': 'bootstrapper.py',
                'log': 'logs/business_generation.json'
            },
            'franchise': {
                'process': 'franchise_engine.py', 
                'log': 'logs/franchise_expansion.json'
            },
            'revenue': {
                'process': 'revenue_optimizer.py',
                'log': 'logs/revenue_optimization.json'
            }
        }
        
    def check_running(self):
        """Check which systems are running"""
        running = {}
        for name, info in self.systems.items():
            try:
                result = subprocess.run(
                    ['pgrep', '-f', info['process']],
                    capture_output=True,
                    text=True
                )
                running[name] = result.returncode == 0
            except:
                running[name] = False
        return running
    
    def get_latest_entries(self):
        """Get latest entries from logs"""
        entries = {}
        for name, info in self.systems.items():
            log_file = info['log']
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            entries[name] = json.loads(lines[-1])
                except:
                    entries[name] = None
            else:
                entries[name] = None
        return entries
    
    def display(self):
        """Display dashboard"""
        os.system('clear')
        print("🚀 GODHEAD COMMERCIAL SYSTEMS")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        running = self.check_running()
        entries = self.get_latest_entries()
        
        print("🔄 SYSTEM STATUS:")
        for name, is_running in running.items():
            status = "✅ RUNNING" if is_running else "❌ STOPPED"
            print(f"   {name.upper():12} {status}")
        print()
        
        print("📊 LATEST ACTIVITY:")
        for name, entry in entries.items():
            if entry:
                cycle = entry.get('cycle', '?')
                if name == 'business':
                    concept = entry.get('business_concept', {})
                    print(f"   🏗️  BUSINESS: Cycle {cycle} - {concept.get('concept', 'Unknown')}")
                elif name == 'franchise':
                    print(f"   🔄 FRANCHISE: Cycle {cycle} - Score: {entry.get('franchise_potential', {}).get('replication_score', '?')}")
                elif name == 'revenue':
                    print(f"   💰 REVENUE: Cycle {cycle} - +{entry.get('optimization_strategy', {}).get('estimated_revenue_increase', '?')}")
            else:
                print(f"   ⏳ {name.upper():12} Waiting for data...")
        print()
        print("🔄 Auto-refresh every 5 seconds...")
        print("   Press Ctrl+C to exit")

# Start dashboard
if __name__ == "__main__":
    dashboard = SimpleDashboard()
    try:
        while True:
            dashboard.display()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
