# CrystalClearHouse

An intelligent agent orchestration system.

## Setup

### 1. Create Virtual Environment and Install Package

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest supervisor
```

### 2. Directory Structure

```
CrystalClearHouse/
├── src/crystalclearhouse/
│   ├── orchestrator/      # Main orchestrator
│   ├── agents/           # Agent implementations
│   └── memory/           # Memory management
├── automation/
│   ├── supervisord/
│   │   ├── supervisord.ini
│   │   └── programs/
│   │       ├── orchestrator.conf
│   │       ├── planner.conf
│   │       └── group-crystalclearhouse.conf
│   └── refresh_all_agents.sh
└── tests/                # Test suite
```

### 3. Start Supervisor and Check Agents

```bash
# Activate virtual environment
source .venv/bin/activate

# Start supervisor
supervisord -c automation/supervisord/supervisord.ini

# Check agent status
supervisorctl -c automation/supervisord/supervisord.ini status
```

### 4. Run Tests

```bash
pytest
```

## Management Commands

### Refresh All Agents

```bash
./automation/refresh_all_agents.sh
```

### Stop Supervisor

```bash
supervisorctl -c automation/supervisord/supervisord.ini shutdown
```

### View Logs

Logs are stored in `/tmp/`:
- `/tmp/orchestrator.out.log` - Orchestrator stdout
- `/tmp/orchestrator.err.log` - Orchestrator stderr
- `/tmp/planner.out.log` - Planner stdout
- `/tmp/planner.err.log` - Planner stderr

## Development

### Running Individual Agents

```bash
# Run orchestrator
crystalclearhouse-orchestrator

# Run planner
crystalclearhouse-planner
```
