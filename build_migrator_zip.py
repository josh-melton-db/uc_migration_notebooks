#!/usr/bin/env python3
"""
Build script to create a migrator ZIP distribution from UCX source code.

This script creates a source-only ZIP file that can be imported into Databricks
workspaces without requiring CLI installation. The package is renamed from 'ucx'
to 'migrator' for a friendlier import experience.

Usage:
    python build_migrator_zip.py

Output:
    migrator_dist.zip - Ready to import into Databricks
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def create_package_structure(temp_dir: Path):
    """Create the basic package structure with renamed imports."""
    print("🏗️  Creating package structure...")
    
    # Create the main package directories
    package_root = temp_dir / "databricks" / "labs" / "migrator"
    package_root.mkdir(parents=True, exist_ok=True)
    
    # Create the convenience import at the top level
    migrator_root = temp_dir / "migrator"
    migrator_root.mkdir(exist_ok=True)
    
    return package_root, migrator_root


def copy_source_files(source_root: Path, package_root: Path):
    """Copy UCX source files to the package root, excluding test files."""
    print("📁 Copying source files...")
    
    ucx_source = source_root / "src" / "databricks" / "labs" / "ucx"
    if not ucx_source.exists():
        raise FileNotFoundError(f"UCX source directory not found: {ucx_source}")
    
    # Copy all Python files and resources
    shutil.copytree(ucx_source, package_root, dirs_exist_ok=True)
    
    # Also copy the main databricks.labs.__init__.py files
    labs_init = source_root / "src" / "databricks" / "labs" / "__init__.py"
    databricks_init = source_root / "src" / "databricks" / "__init__.py"
    
    if labs_init.exists():
        shutil.copy2(labs_init, package_root.parent / "__init__.py")
    if databricks_init.exists():
        shutil.copy2(databricks_init, package_root.parent.parent / "__init__.py")
    
    print(f"   ✅ Copied source files from {ucx_source}")


def create_import_shims(temp_dir: Path, migrator_root: Path, package_root: Path):
    """Create import shims for convenient access."""
    print("🔗 Creating import shims...")
    
    # Create migrator/__init__.py for top-level imports
    migrator_init = migrator_root / "__init__.py"
    migrator_init.write_text('''"""
Migrator - Unity Catalog Migration Toolkit

A renamed version of UCX for easy import into Databricks workspaces.
"""

# Main installer for assessment workflows
from databricks.labs.migrator.install import WorkspaceInstaller as assessment

# Common utilities
from databricks.labs.migrator.install import WorkspaceInstaller
from databricks.labs.migrator.config import WorkspaceConfig

__all__ = ['assessment', 'WorkspaceInstaller', 'WorkspaceConfig']
''')
    
    # Update the main package __init__.py to reflect the name change
    package_init = package_root / "__init__.py"
    if package_init.exists():
        content = package_init.read_text()
        # Replace references to 'ucx' with 'migrator' in the init file
        content = content.replace('"ucx"', '"migrator"')
        content = content.replace("'ucx'", "'migrator'")
        package_init.write_text(content)
    
    print("   ✅ Created import shims")


def update_internal_references(package_root: Path):
    """Update internal package references from ucx to migrator."""
    print("🔄 Updating internal references...")
    
    python_files = list(package_root.rglob("*.py"))
    updated_count = 0
    
    for py_file in python_files:
        try:
            content = py_file.read_text(encoding='utf-8')
            original_content = content
            
            # Replace import statements
            content = content.replace("from databricks.labs.ucx", "from databricks.labs.migrator")
            content = content.replace("import databricks.labs.ucx", "import databricks.labs.migrator")
            content = content.replace("databricks.labs.ucx.", "databricks.labs.migrator.")
            
            # Replace string references that might be used in configuration
            content = content.replace('"ucx"', '"migrator"')
            content = content.replace("'ucx'", "'migrator'")
            content = content.replace('product="ucx"', 'product="migrator"')
            content = content.replace("product_name() == 'ucx'", "product_name() == 'migrator'")
            content = content.replace('self.product_info.product_name()', "'migrator'")
            
            if content != original_content:
                py_file.write_text(content, encoding='utf-8')
                updated_count += 1
                
        except Exception as e:
            print(f"   ⚠️  Warning: Could not update {py_file}: {e}")
    
    print(f"   ✅ Updated {updated_count} Python files")


def create_installation_script(temp_dir: Path):
    """Create the installation Python script for easy setup."""
    print("🐍 Creating installation script...")
    
    script_content = '''#!/usr/bin/env python3
"""
Migrator Installation Script

This script installs the Migrator (UCX) assessment workflows into your Databricks workspace.

Prerequisites:
1. Workspace Admin privileges
2. A PRO or Serverless SQL Warehouse
3. Import the migrator ZIP file into your workspace
4. Run this script in a Databricks notebook or Python environment

Usage:
    python install_migrator.py

Instructions:
1. Run this script in a Databricks environment
2. Follow the prompts to configure your installation
3. The assessment workflow will be created and can be run from the Jobs UI
"""

import sys
import os
import traceback


def install_dependencies():
    """Install required dependencies for the migrator."""
    print("📦 Installing required dependencies...")
    print("This may take a few minutes on first run.")
    
    try:
        # Check if we're in Databricks environment
        import dbutils
        # Use Databricks pip magic command
        dbutils.library.installPyPI("databricks-sdk", version=">=0.58.0,<0.59.0")
        dbutils.library.installPyPI("databricks-labs-lsql", version=">=0.16.0,<0.17.0")
        dbutils.library.installPyPI("databricks-labs-blueprint", version=">=0.11.0,<0.12.0")
        dbutils.library.installPyPI("PyYAML", version=">=6.0.0,<6.1.0")
        dbutils.library.installPyPI("sqlglot", version=">=26.7.0,<27.1.0")
        dbutils.library.installPyPI("astroid", version=">=3.3.0,<3.4.0")
        
        # Restart Python to ensure packages are available
        dbutils.library.restartPython()
        print("✅ Dependencies installed and Python restarted")
        
    except ImportError:
        # Not in Databricks environment, use regular pip
        import subprocess
        
        packages = [
            "databricks-sdk>=0.58.0,<0.59.0",
            "databricks-labs-lsql>=0.16.0,<0.17.0", 
            "databricks-labs-blueprint>=0.11.0,<0.12.0",
            "PyYAML>=6.0.0,<6.1.0",
            "sqlglot>=26.7.0,<27.1.0",
            "astroid>=3.3.0,<3.4.0"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ Dependencies installed successfully")


def setup_python_path():
    """Add the migrator package to Python path."""
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"✅ Added {current_dir} to Python path")
    else:
        print(f"ℹ️  {current_dir} already in Python path")


def import_migrator():
    """Import and validate migrator package."""
    try:
        from databricks.sdk import WorkspaceClient
        import migrator
        
        print("✅ Successfully imported migrator package")
        print("📋 Available components:")
        print("   - migrator.assessment: Main installer class")
        print("   - migrator.WorkspaceInstaller: Direct installer access")
        print("   - migrator.WorkspaceConfig: Configuration class")
        
        return WorkspaceClient, migrator
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("")
        print("🔧 Try installing missing dependencies by running:")
        print("   pip install databricks-sdk databricks-labs-lsql databricks-labs-blueprint PyYAML sqlglot astroid")
        print("   Then restart this script.")
        raise


def initialize_installer(WorkspaceClient, migrator):
    """Initialize the workspace client and installer."""
    print("🔧 Initializing Databricks workspace client...")
    workspace_client = WorkspaceClient()

    print("🚀 Initializing Migrator installer...")
    installer = migrator.assessment(workspace_client)

    print("✅ Installer ready!")
    print(f"🏢 Connected to workspace: {workspace_client.config.host}")
    
    return workspace_client, installer


def run_installation(workspace_client, installer):
    """Run the installation with interactive prompts."""
    print("🎯 Starting Migrator installation...")
    print("📝 You will be prompted for configuration options.")
    print("")

    try:
        # This will prompt for configuration and install the workflows
        config = installer.run()
        
        print("")
        print("🎉 Installation completed successfully!")
        print("")
        print("📊 Next steps:")
        print("   1. Go to the Jobs UI in your Databricks workspace")
        print("   2. Find the 'Migrator - Assessment' workflow")
        print("   3. Run the assessment to analyze your workspace")
        print("   4. View results in the generated dashboards")
        print("")
        print(f"🌐 Installation folder: {config.inventory_database}")
        print(f"🏢 Workspace: {workspace_client.config.host}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("")
        print("🔧 Try installing missing dependencies:")
        print("   pip install databricks-sdk databricks-labs-lsql databricks-labs-blueprint PyYAML sqlglot astroid")
        print("   Then restart this script and try again.")
        return False
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        print("")
        print("🔍 Troubleshooting tips:")
        print("   - Ensure you have Workspace Admin privileges")
        print("   - Verify you have a PRO or Serverless SQL Warehouse available")
        print("   - Check that all dependencies are properly installed")
        print("   - Verify your cluster has internet access for installation")
        
        # Show the specific error for debugging
        print("")
        print("🐛 Full error details:")
        traceback.print_exc()
        return False


def print_success_info():
    """Print information about what was installed."""
    print("\\n" + "=" * 60)
    print("📋 What was installed?")
    print("=" * 60)
    print("")
    print("The Migrator installation creates:")
    print("")
    print("1. 📊 Assessment Workflow: A Databricks job that analyzes your workspace")
    print("   for Unity Catalog migration readiness")
    print("")
    print("2. 🗄️  Database: A Hive Metastore database to store assessment results")
    print("")
    print("3. 📈 Dashboards: Interactive dashboards to visualize assessment findings")
    print("")
    print("4. ⚙️  Configuration: Workspace-level configuration for the migration toolkit")
    print("")
    print("=" * 60)
    print("🚀 Running Assessments")
    print("=" * 60)
    print("")
    print("After installation, you can:")
    print("• Run the assessment workflow from the Jobs UI")
    print("• View results in the automatically created dashboards")
    print("• Use the migrator programmatically:")
    print("")
    print("    import migrator")
    print("    from databricks.sdk import WorkspaceClient")
    print("    migrator.assessment(WorkspaceClient()).run()")
    print("")
    print("=" * 60)
    print("🆘 Support")
    print("=" * 60)
    print("")
    print("For issues or questions:")
    print("• Check the installation output above for error details")
    print("• Review the assessment dashboard for guidance")
    print("• Verify all prerequisites are met")
    print("• Consult with your Databricks team")


def main():
    """Main installation function."""
    print("🚀 Migrator Installation Script")
    print("=" * 50)
    print("")
    
    try:
        # Step 1: Install dependencies (if needed)
        try:
            # Try importing first - dependencies might already be available
            from databricks.sdk import WorkspaceClient
            import migrator
            print("✅ Dependencies already available")
        except ImportError:
            install_dependencies()
        
        # Step 2: Setup Python path
        setup_python_path()
        
        # Step 3: Import migrator
        WorkspaceClient, migrator = import_migrator()
        
        # Step 4: Initialize installer
        workspace_client, installer = initialize_installer(WorkspaceClient, migrator)
        
        # Step 5: Run installation
        success = run_installation(workspace_client, installer)
        
        # Step 6: Show success information
        if success:
            print_success_info()
        
        return success
        
    except Exception as e:
        print(f"\\n❌ Installation script failed: {e}")
        print("\\n🔍 Please check the error details above and ensure:")
        print("   - You're running this in a Databricks environment")
        print("   - You have Workspace Admin privileges")
        print("   - All prerequisites are met")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 Installation completed successfully!")
    else:
        print("\\n💔 Installation failed. Please review the errors above.")
        sys.exit(1)
'''
    
    script_path = temp_dir / "install_migrator.py"
    script_path.write_text(script_content)
    
    print(f"   ✅ Created installation script: {script_path.name}")


def create_readme(temp_dir: Path):
    """Create a README file with usage instructions."""
    print("📖 Creating README...")
    
    readme_content = """# Migrator Distribution

This ZIP file contains a source-only distribution of the Migrator (UCX) Unity Catalog migration toolkit, renamed for easy import into Databricks workspaces.

## Quick Start

1. **Import into Databricks:**
   - Go to Workspace → Import in your Databricks UI
   - Choose "Source" format and upload this ZIP file
   - The files will be extracted to `/Workspace/migrator_dist/`

2. **Run the installation script:**
   - Open `install_migrator.py` in a Databricks notebook
   - Run the script and follow the prompts
   - This will set up the assessment workflows in your workspace

3. **Use in your notebooks:**
   ```python
   import sys
   sys.path.insert(0, '/Workspace/migrator_dist')
   
   import migrator
   # migrator.assessment is now available
   ```

## What's Included

- **migrator/** - Main package with all UCX functionality renamed
- **databricks/labs/migrator/** - Full source code
- **install_migrator.py** - Installation script
- **README.md** - This file

## Requirements

- Databricks Premium or Enterprise workspace
- Workspace Admin privileges
- PRO or Serverless SQL Warehouse
- Python 3.10+ (automatically available in DBR)

## Installation Options

### Option 1: Add to cluster libraries (Recommended)
1. Go to your cluster configuration
2. Libraries → Install New → Upload → Python
3. Upload this ZIP file
4. Restart cluster
5. All notebooks on this cluster can now `import migrator`

### Option 2: Per-notebook import
```python
import sys
sys.path.insert(0, '/Workspace/migrator_dist')
import migrator
```

## One-liner Usage

After setup, you can install assessment workflows with:

```python
import migrator
from databricks.sdk import WorkspaceClient

migrator.assessment(WorkspaceClient()).run()
```

## Dependencies

This distribution includes all UCX source code but requires external dependencies. The installation notebook will automatically install these, but you can also install them manually:

### Required Packages:
- `databricks-sdk>=0.58.0,<0.59.0` - Databricks SDK
- `databricks-labs-lsql>=0.16.0,<0.17.0` - SQL backends and dashboards  
- `databricks-labs-blueprint>=0.11.0,<0.12.0` - Installation and utilities framework
- `PyYAML>=6.0.0,<6.1.0` - YAML configuration handling
- `sqlglot>=26.7.0,<27.1.0` - SQL parsing and analysis
- `astroid>=3.3.0,<3.4.0` - Python code analysis

### Manual Installation:
```python
%pip install databricks-sdk>=0.58.0,<0.59.0 databricks-labs-lsql>=0.16.0,<0.17.0 databricks-labs-blueprint>=0.11.0,<0.12.0 PyYAML>=6.0.0,<6.1.0 sqlglot>=26.7.0,<27.1.0 astroid>=3.3.0,<3.4.0
dbutils.library.restartPython()
```

## Support

This is a source distribution based on the open-source UCX project. For support:
- Review the installation notebook output
- Check generated dashboards for guidance
- Consult the original UCX documentation
"""
    
    readme_path = temp_dir / "README.md"
    readme_path.write_text(readme_content)
    
    print(f"   ✅ Created README: {readme_path.name}")


def copy_essential_dependencies(temp_dir: Path):
    """Copy or create stubs for essential dependencies that might not be available."""
    print("📦 Handling dependencies...")
    
    # Create a simple requirements marker file
    requirements_path = temp_dir / "REQUIREMENTS.txt"
    requirements_content = """# External dependencies required for migrator
# These should be available in Databricks Runtime or can be installed via %pip

databricks-sdk>=0.58.0,<0.59.0
databricks-labs-lsql>=0.16.0,<0.17.0
databricks-labs-blueprint>=0.11.0,<0.12.0
PyYAML>=6.0.0,<6.1.0
sqlglot>=26.7.0,<27.1.0
astroid>=3.3.0,<3.4.0

# Installation command if needed:
# %pip install -r REQUIREMENTS.txt
"""
    requirements_path.write_text(requirements_content)
    
    print("   ✅ Created REQUIREMENTS.txt")


def create_zip_distribution(temp_dir: Path, output_path: Path):
    """Create the final ZIP distribution."""
    print("📦 Creating ZIP distribution...")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                # Calculate the archive path relative to temp_dir
                archive_path = file_path.relative_to(temp_dir)
                zipf.write(file_path, archive_path)
    
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"   ✅ Created {output_path} ({file_size:.1f} MB)")


def main():
    """Main build process."""
    print("🚀 Building Migrator ZIP Distribution")
    print("=" * 50)
    
    # Get the project root (where this script is located)
    script_dir = Path(__file__).parent.absolute()
    output_path = script_dir / "migrator_dist.zip"
    
    # Clean up any existing output
    if output_path.exists():
        output_path.unlink()
        print(f"🗑️  Removed existing {output_path.name}")
    
    # Create temporary directory for building
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print(f"🏗️  Working in temporary directory: {temp_dir}")
        
        try:
            # Build the package
            package_root, migrator_root = create_package_structure(temp_dir)
            copy_source_files(script_dir, package_root)
            create_import_shims(temp_dir, migrator_root, package_root)
            update_internal_references(package_root)
            create_installation_script(temp_dir)
            create_readme(temp_dir)
            copy_essential_dependencies(temp_dir)
            create_zip_distribution(temp_dir, output_path)
            
            print("\n" + "=" * 50)
            print("✅ Build completed successfully!")
            print(f"📦 Output: {output_path}")
            print(f"📏 Size: {output_path.stat().st_size / (1024 * 1024):.1f} MB")
            print("\n🎯 Next steps:")
            print("   1. Upload migrator_dist.zip to Databricks workspace")
            print("   2. Run install_migrator.py script")
            print("   3. Start using migrator.assessment for migrations!")
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            raise


if __name__ == "__main__":
    main() 