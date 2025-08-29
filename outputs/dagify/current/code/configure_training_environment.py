from ._configure_training_environment.install_framework_dependencies import install_framework_dependencies
from ._configure_training_environment.configure_hardware_environment import configure_hardware_environment
from ._configure_training_environment.setup_distributed_environment import setup_distributed_environment
from ._configure_training_environment.determine_containerization_need import determine_containerization_need
from ._configure_training_environment.setup_containerized_environment import setup_containerized_environment
from ._configure_training_environment.validate_environment_setup import validate_environment_setup

from pydantic import BaseModel, Field
from typing import List


class SelectTrainingFrameworkOutput(BaseModel):
    """Pydantic model for select_training_framework node outputs."""
    selected_framework: str = Field(..., description="Selected machine learning framework")
    selected_toolkit: str = Field(..., description="Selected distributed training toolkit")
    hardware_resources: str = Field(..., description="List of selected hardware resources")
    training_plan: str = Field(..., description="Detailed training plan with epoch count, batch size, and learning rate")


class ConfigureTrainingEnvironmentOutput(BaseModel):
    """Pydantic model for configure_training_environment node outputs."""
    environment_settings: List[str] = Field(..., description="List of environment settings, including installed libraries and dependencies.")
    containerized_environment: bool = Field(..., description="Whether the environment is containerized.")
    training_environment_status: str = Field(..., description="Status of the training environment, including any errors or warnings.")


def configure_training_environment(select_training_framework_input: SelectTrainingFrameworkOutput, **kwargs) -> ConfigureTrainingEnvironmentOutput:
    """Set up software environment with dependencies, libraries, and containerization tools for training.

    Args:
        select_training_framework_input: Input from the 'select_training_framework' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ConfigureTrainingEnvironmentOutput: Object containing outputs for this node.
    """
    # Install framework-specific dependencies and libraries
    framework_dependencies: List[str] = install_framework_dependencies(
        framework=select_training_framework_input.selected_framework,
        toolkit=select_training_framework_input.selected_toolkit
    )
    
    # Configure hardware-specific drivers and libraries
    hardware_settings: List[str] = configure_hardware_environment(
        hardware_resources=select_training_framework_input.hardware_resources
    )
    
    # Set up distributed training environment if needed
    distributed_settings: List[str] = setup_distributed_environment(
        toolkit=select_training_framework_input.selected_toolkit,
        hardware_resources=select_training_framework_input.hardware_resources
    )
    
    # Determine if containerization is needed and set it up
    should_containerize: bool = determine_containerization_need(
        framework=select_training_framework_input.selected_framework,
        hardware_resources=select_training_framework_input.hardware_resources
    )
    
    container_settings: List[str] = []
    if should_containerize:
        container_settings = setup_containerized_environment(
            framework=select_training_framework_input.selected_framework,
            dependencies=framework_dependencies
        )
    
    # Validate environment setup and check for conflicts
    validation_result: str = validate_environment_setup(
        framework_deps=framework_dependencies,
        hardware_settings=hardware_settings,
        distributed_settings=distributed_settings,
        container_settings=container_settings
    )
    
    # Combine all environment settings
    all_environment_settings: List[str] = framework_dependencies + hardware_settings + distributed_settings + container_settings
    
    return ConfigureTrainingEnvironmentOutput(
        environment_settings=all_environment_settings,
        containerized_environment=should_containerize,
        training_environment_status=validation_result
    )