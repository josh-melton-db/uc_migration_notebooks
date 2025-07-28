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

# Now import the key classes directly from the migrator package (no databricks.labs prefix needed)
try:
    from migrator.installer.workflows import WorkspaceInstaller
    from migrator.contexts.workflow_task import WorkspaceConfig
    
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
    import os
    import sys
    
    # Capture the error message for later use
    _import_error_message = str(e)
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def assessment(workspace_client):
        raise ImportError(
            f"Failed to import migrator components: {_import_error_message}\n"
            f"Current directory: {_current_dir}\n"
            f"Python path: {sys.path[:3]}...\n"
            "Please ensure the migrator package is properly installed."
        )
    
    def WorkspaceInstaller(workspace_client):
        raise ImportError(f"Failed to import WorkspaceInstaller: {_import_error_message}")
    
    def WorkspaceConfig(workspace_client):
        raise ImportError(f"Failed to import WorkspaceConfig: {_import_error_message}")
    
    __all__ = ['assessment', 'WorkspaceInstaller', 'WorkspaceConfig']
