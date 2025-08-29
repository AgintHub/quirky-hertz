from pydantic import BaseModel, Field


class DefineModelSpecificationsOutput(BaseModel):
    """Pydantic model for define_model_specifications node outputs."""
    model_name: str = Field(..., description="Name of the GPT-6 model")
    model_size: int = Field(..., description="Number of parameters in the GPT-6 model")
    model_modality: str = Field(..., description="Type of input data for the GPT-6 model (e.g., text, code)")
    model_architecture: str = Field(..., description="Architecture of the GPT-6 model")
    expected_capabilities: str = Field(..., description="Expected capabilities of the GPT-6 model for deep learning with code")


class SelectHardwareInfrastructureOutput(BaseModel):
    """Pydantic model for select_hardware_infrastructure node outputs."""
    hardware_infrastructure_type: str = Field(..., description="Type of hardware infrastructure selected (e.g., GPU, TPU, CPU)")
    number_of_nodes: int = Field(..., description="Number of nodes in the hardware infrastructure")
    memory_required: str = Field(..., description="Memory requirements of the hardware infrastructure (e.g., in GB)")
    storage_required: str = Field(..., description="Storage requirements of the hardware infrastructure (e.g., in GB)")
    reasoning_description: str = Field(..., description="Description of the reasoning behind the selected hardware infrastructure")


def select_hardware_infrastructure(define_model_specifications_input: DefineModelSpecificationsOutput, **kwargs) -> SelectHardwareInfrastructureOutput:
    """Decide on computing resources for model training including GPUs/TPUs and storage.

    Args:
        define_model_specifications_input: Input from the 'define_model_specifications' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SelectHardwareInfrastructureOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SelectHardwareInfrastructureOutput(
        hardware_infrastructure_type="",
        number_of_nodes=0,
        memory_required="",
        storage_required="",
        reasoning_description="",
    )