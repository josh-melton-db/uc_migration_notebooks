# Migrator - Unity Catalog Migration Toolkit

A simple, notebook-driven Unity Catalog migration toolkit for Databricks workspaces.

## Quick Start

### 1. Upload to Databricks
- Go to your Databricks workspace
- Navigate to **Workspace** → **Import** 
- Select **Source** format and upload `migrator_dist.zip`
- Files will be extracted to `/Workspace/migrator_dist/`

### 2. Run Installation
- Open the `install_migrator.py` script in a Databricks notebook
- Run the script (dependencies install automatically)
- Follow the interactive prompts to configure your migration

### 3. Start Assessment
```python
import migrator
from databricks.sdk import WorkspaceClient

migrator.assessment(WorkspaceClient()).run()
```

## What Gets Installed

The migrator creates:
- **Assessment Workflow**: Analyzes your workspace for Unity Catalog readiness
- **Migration Database**: Stores assessment results and migration progress  
- **Interactive Dashboards**: Visualizes migration findings and recommendations
- **Configuration**: Workspace-level settings for the migration toolkit

## Requirements

- Databricks Premium or Enterprise workspace
- Workspace Admin privileges
- PRO or Serverless SQL Warehouse
- Python 3.10+ (available in Databricks Runtime)

## Installation Options

### Option A: Cluster Libraries (Recommended)
1. Go to your cluster configuration
2. **Libraries** → **Install New** → **Upload** → **Python**
3. Upload `migrator_dist.zip`
4. Restart cluster
5. All notebooks can now `import migrator`

### Option B: Per-Notebook Import
```python
import sys
sys.path.insert(0, '/Workspace/migrator_dist')
import migrator
```

## Next Steps

After installation:
1. Go to **Jobs** in your Databricks workspace
2. Find and run the **Migrator - Assessment** workflow  
3. View results in the auto-generated dashboards
4. Follow dashboard recommendations for migration planning

## Troubleshooting

**Import errors?**
```python
%pip install databricks-sdk databricks-labs-lsql databricks-labs-blueprint PyYAML sqlglot astroid
dbutils.library.restartPython()
```

**Installation fails?**
- Ensure you have Workspace Admin privileges
- Verify you have a PRO or Serverless SQL Warehouse available
- Check that your cluster has internet access

**Need help?**
- Review the installation notebook output for detailed error messages
- Check the generated dashboards for migration guidance
- Verify all prerequisites are met

---

*This toolkit helps migrate Databricks workspaces to Unity Catalog with minimal complexity.*