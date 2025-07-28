#!/usr/bin/env python3
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
    # Get the current directory - works in both script and notebook environments
    try:
        # Try to get the script directory first (works in regular Python scripts)
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # __file__ is not defined in Databricks notebooks, use current working directory
        current_dir = os.getcwd()
        print(f"ℹ️  Running in notebook environment, using current directory: {current_dir}")
    
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
    print("\n" + "=" * 60)
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
        print(f"\n❌ Installation script failed: {e}")
        print("\n🔍 Please check the error details above and ensure:")
        print("   - You're running this in a Databricks environment")
        print("   - You have Workspace Admin privileges")
        print("   - All prerequisites are met")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Installation completed successfully!")
    else:
        print("\n💔 Installation failed. Please review the errors above.")
        sys.exit(1)
