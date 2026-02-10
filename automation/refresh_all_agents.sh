#!/bin/bash
# Script to refresh all CrystalClearHouse agents via Supervisor

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SUPERVISOR_CONFIG="$PROJECT_ROOT/automation/supervisord/supervisord.ini"

echo "=== Refreshing CrystalClearHouse Agents ==="

# Check if supervisor is running
if supervisorctl -c "$SUPERVISOR_CONFIG" status > /dev/null 2>&1; then
    echo "✓ Supervisor is running"
    
    # Restart all agents in the crystalclearhouse group
    echo "Restarting agents..."
    supervisorctl -c "$SUPERVISOR_CONFIG" restart crystalclearhouse:*
    
    echo ""
    echo "Current status:"
    supervisorctl -c "$SUPERVISOR_CONFIG" status
else
    echo "✗ Supervisor is not running"
    echo "Start supervisor with: supervisord -c $SUPERVISOR_CONFIG"
    exit 1
fi

echo ""
echo "=== Refresh Complete ==="
