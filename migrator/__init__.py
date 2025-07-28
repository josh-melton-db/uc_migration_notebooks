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

# Import key classes from the migrator package
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