# Migrator - Unity Catalog Migration Toolkit

A simple, notebook-driven Unity Catalog migration toolkit for Databricks workspaces.

## Quick Start

### 1. Upload to Databricks
- Go to your Databricks workspace
- Navigate to **Workspace** → **Import** 
- Select **Source** format and upload `migrator_dist.zip`
- Files will be extracted to `/Workspace/migrator_dist/`

### 2. Run Installation

The migrator includes an interactive installation script that automatically handles dependency management and configuration.

#### Using the Installation Script

**Option A: Automatic dependency installation (Recommended)**
```python
# In a Databricks notebook, simply run:
%run ./install_migrator
```

**Option B: Manual dependency installation**
```python
# Install dependencies first
%pip install -r requirements.txt
dbutils.library.restartPython()

# Then run the installer
%run ./install_migrator
```

**Option C: Command line (for Python environments)**
```bash
# Automatic installation
python install_migrator.py

# Or install dependencies manually first
pip install -r requirements.txt
python install_migrator.py
```

#### What the Installation Script Does

The `install_migrator.py` script automatically:
1. **📦 Installs Dependencies**: All required packages (databricks-sdk, lsql, blueprint, etc.)
2. **🔧 Configures Python Path**: Sets up the migrator package for import
3. **🚀 Initializes Workspace Client**: Connects to your Databricks workspace
4. **📝 Interactive Configuration**: Prompts for installation settings
5. **⚙️ Creates Workflows**: Sets up assessment jobs and dashboards
6. **✅ Validates Installation**: Ensures everything is properly configured

The script provides detailed progress updates and troubleshooting guidance throughout the process.

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

### Option C: Direct Installation Script Usage

The installation script works in multiple environments:

**Databricks Notebooks (Recommended):**
```python
%run ./install_migrator
```

**Databricks Python Environments:**
```python
exec(open('install_migrator.py').read())
```

**Local Python (for testing/development):**
```bash
python install_migrator.py
```

## Installation Script Features

The `install_migrator.py` script includes:

- ✅ **Automatic Dependency Management**: Installs all required packages
- 🔍 **Environment Detection**: Works in notebooks and Python scripts
- 📦 **Package Validation**: Verifies migrator package structure
- 🏢 **Workspace Connection**: Automatic Databricks workspace client setup
- 📝 **Interactive Prompts**: Guides you through configuration options
- 🛠️ **Error Handling**: Comprehensive troubleshooting and validation
- 📊 **Progress Updates**: Real-time feedback during installation

### Script Output
The installation script provides detailed feedback:
```
🚀 Migrator Installation Script
==================================================

📦 Installing required dependencies...
✅ Dependencies installed successfully
✅ Added /path/to/migrator to Python path
🔍 Checking package structure:
   - migrator/ exists: True
✅ Package structure verified
✅ Successfully imported databricks-sdk
✅ Successfully imported migrator package
🔧 Initializing Databricks workspace client...
🚀 Initializing Migrator installer...
✅ Installer ready!
🏢 Connected to workspace: https://your-workspace.cloud.databricks.com
```

## Next Steps

After installation:
1. Go to **Jobs** in your Databricks workspace
2. Find and run the **Migrator - Assessment** workflow  
3. View results in the auto-generated dashboards
4. Follow dashboard recommendations for migration planning

## Troubleshooting

**Import errors during installation?**
The installation script automatically handles dependencies, but if you encounter issues:
```python
%pip install databricks-sdk>=0.58.0,<0.59.0 databricks-labs-lsql>=0.16.0,<0.17.0 databricks-labs-blueprint>=0.11.0,<0.12.0 PyYAML>=6.0.0,<6.1.0 sqlglot>=26.7.0,<27.1.0 astroid>=3.3.0,<3.4.0
dbutils.library.restartPython()
```

**Installation script fails?**
The script provides detailed error information. Common issues:
- Ensure you have Workspace Admin privileges
- Verify you have a PRO or Serverless SQL Warehouse available
- Check that your cluster has internet access
- Confirm the migrator package structure exists

**Package structure issues?**
```python
# Check if files extracted properly
import os
print("Current directory:", os.getcwd())
print("Contents:", os.listdir('.'))
print("Migrator exists:", os.path.exists('./migrator'))
```

**Need help?**
- Review the installation script output for detailed error messages
- Check the generated dashboards for migration guidance
- Verify all prerequisites are met
- The installation script provides comprehensive troubleshooting tips

---

*This toolkit helps migrate Databricks workspaces to Unity Catalog with minimal complexity.*