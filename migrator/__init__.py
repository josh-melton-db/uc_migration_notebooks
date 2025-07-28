"""
Migrator - Unity Catalog Migration Toolkit

A simplified interface to the Unity Catalog migration assessment and migration tools.

Usage:
    import migrator
    from databricks.sdk import WorkspaceClient
    
    # Run assessment
    migrator.assessment(WorkspaceClient()).run()
    
    # Or access components directly
    installer = migrator.WorkspaceInstaller(WorkspaceClient())
    config = migrator.WorkspaceConfig(WorkspaceClient())
"""

import sys
import os

# Ensure the databricks.labs.migrator package can be found
# Get the parent directory of this migrator package
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)

# Add the parent directory to Python path if not already there
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Now import the key classes from the migrator package
try:
    from databricks.labs.migrator.installer.workflows import WorkspaceInstaller
    from databricks.labs.migrator.contexts.workflow_task import WorkspaceConfig
    
    # Convenience function for the main use case
    def assessment(workspace_client):
        """
        Create a WorkspaceInstaller instance for running assessments.
        
        Args:
            workspace_client: A databricks.sdk.WorkspaceClient instance
            
        Returns:
            WorkspaceInstaller instance ready to run assessments
        """
        return WorkspaceInstaller(workspace_client)
    
    # Export main classes for direct access
    __all__ = ['assessment', 'WorkspaceInstaller', 'WorkspaceConfig']
    
except ImportError as e:
    # If imports fail, provide a helpful error message
    def assessment(workspace_client):
        raise ImportError(
            f"Failed to import migrator components: {e}\n"
            f"Current directory: {_current_dir}\n"
            f"Parent directory: {_parent_dir}\n"
            f"Python path: {sys.path[:3]}...\n"
            "Please ensure the databricks/labs/migrator package is properly installed."
        )
    
    def WorkspaceInstaller(workspace_client):
        raise ImportError(f"Failed to import WorkspaceInstaller: {e}")
    
    def WorkspaceConfig(workspace_client):
        raise ImportError(f"Failed to import WorkspaceConfig: {e}")
    
    __all__ = ['assessment', 'WorkspaceInstaller', 'WorkspaceConfig'] 