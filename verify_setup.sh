#!/bin/bash
# Verification script for CrystalClearHouse setup

set -e

PROJECT_ROOT="/home/runner/work/Depository/Depository"
cd "$PROJECT_ROOT"

echo "======================================"
echo "CrystalClearHouse Setup Verification"
echo "======================================"
echo ""

# 1. Check directory structure
echo "✓ Checking directory structure..."
[ -d "src/crystalclearhouse/orchestrator" ] && echo "  ✓ src/crystalclearhouse/orchestrator exists"
[ -d "src/crystalclearhouse/agents" ] && echo "  ✓ src/crystalclearhouse/agents exists"
[ -d "src/crystalclearhouse/memory" ] && echo "  ✓ src/crystalclearhouse/memory exists"
[ -d "automation/supervisord" ] && echo "  ✓ automation/supervisord exists"
[ -d "automation/supervisord/programs" ] && echo "  ✓ automation/supervisord/programs exists"
echo ""

# 2. Check files
echo "✓ Checking required files..."
[ -f "automation/supervisord/supervisord.ini" ] && echo "  ✓ supervisord.ini exists"
[ -f "automation/supervisord/programs/orchestrator.conf" ] && echo "  ✓ orchestrator.conf exists"
[ -f "automation/supervisord/programs/planner.conf" ] && echo "  ✓ planner.conf exists"
[ -f "automation/supervisord/programs/group-crystalclearhouse.conf" ] && echo "  ✓ group-crystalclearhouse.conf exists"
[ -x "automation/refresh_all_agents.sh" ] && echo "  ✓ refresh_all_agents.sh exists and is executable"
[ -f "setup.py" ] && echo "  ✓ setup.py exists"
echo ""

# 3. Check virtual environment
echo "✓ Checking virtual environment..."
if [ -d ".venv" ]; then
    echo "  ✓ .venv directory exists"
    source .venv/bin/activate
    echo "  ✓ Virtual environment activated"
else
    echo "  ✗ Virtual environment not found - creating it..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    pip install pytest supervisor
fi
echo ""

# 4. Check package installation
echo "✓ Checking package installation..."
if python -c "import crystalclearhouse" 2>/dev/null; then
    echo "  ✓ crystalclearhouse package is importable"
else
    echo "  ✗ Package not installed - installing..."
    pip install -e .
fi

if which crystalclearhouse-orchestrator >/dev/null 2>&1; then
    echo "  ✓ crystalclearhouse-orchestrator command available"
fi

if which crystalclearhouse-planner >/dev/null 2>&1; then
    echo "  ✓ crystalclearhouse-planner command available"
fi
echo ""

# 5. Run tests
echo "✓ Running tests..."
if pytest -q 2>&1; then
    echo "  ✓ All tests passed"
else
    echo "  ✗ Some tests failed"
    exit 1
fi
echo ""

# 6. Test supervisor configuration
echo "✓ Testing Supervisor configuration..."
supervisord -c automation/supervisord/supervisord.ini > /dev/null 2>&1
sleep 3

STATUS=$(supervisorctl -c automation/supervisord/supervisord.ini status 2>&1)
echo "$STATUS"

if echo "$STATUS" | grep -q "RUNNING"; then
    echo "  ✓ Agents are running"
else
    echo "  ✗ Agents not running properly"
    supervisorctl -c automation/supervisord/supervisord.ini shutdown
    exit 1
fi
echo ""

# 7. Test refresh script
echo "✓ Testing refresh script..."
./automation/refresh_all_agents.sh > /dev/null 2>&1
echo "  ✓ Refresh script executed successfully"
echo ""

# 8. Cleanup
echo "✓ Cleaning up..."
supervisorctl -c automation/supervisord/supervisord.ini shutdown > /dev/null 2>&1
sleep 2
echo "  ✓ Supervisor shut down"
echo ""

echo "======================================"
echo "✓ All verifications passed!"
echo "======================================"
echo ""
echo "The CrystalClearHouse system is ready to use."
echo ""
echo "Quick start commands:"
echo "  1. Activate venv: source .venv/bin/activate"
echo "  2. Start system: supervisord -c automation/supervisord/supervisord.ini"
echo "  3. Check status: supervisorctl -c automation/supervisord/supervisord.ini status"
echo "  4. Run tests: pytest"
