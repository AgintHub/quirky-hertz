from ._select_hardware_infrastructure.analyze_model_hardware_requirements import analyze_model_hardware_requirements
from ._select_hardware_infrastructure.select_optimal_hardware_type import select_optimal_hardware_type
from ._select_hardware_infrastructure.calculate_optimal_node_count import calculate_optimal_node_count
from ._select_hardware_infrastructure.calculate_memory_requirements import calculate_memory_requirements
from ._select_hardware_infrastructure.calculate_storage_requirements import calculate_storage_requirements
from ._select_hardware_infrastructure.generate_hardware_selection_reasoning import generate_hardware_selection_reasoning

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
    # Analyze model requirements to determine optimal hardware
    hardware_requirements: dict = analyze_model_hardware_requirements(
        model_size=define_model_specifications_input.model_size,
        model_architecture=define_model_specifications_input.model_architecture,
        model_modality=define_model_specifications_input.model_modality
    )
    
    # Select appropriate hardware type based on model specifications
    selected_hardware_type: str = select_optimal_hardware_type(
        requirements=hardware_requirements,
        expected_capabilities=define_model_specifications_input.expected_capabilities
    )
    
    # Calculate required number of nodes for distributed training
    optimal_node_count: int = calculate_optimal_node_count(
        model_size=define_model_specifications_input.model_size,
        hardware_type=selected_hardware_type
    )
    
    # Determine memory requirements for training
    memory_specs: str = calculate_memory_requirements(
        model_size=define_model_specifications_input.model_size,
        node_count=optimal_node_count,
        hardware_type=selected_hardware_type
    )
    
    # Determine storage requirements for model and data
    storage_specs: str = calculate_storage_requirements(
        model_size=define_model_specifications_input.model_size,
        model_modality=define_model_specifications_input.model_modality,
        training_data_estimate=hardware_requirements
    )
    
    # Generate reasoning for hardware selection decisions
    reasoning: str = generate_hardware_selection_reasoning(
        model_specs=define_model_specifications_input,
        hardware_type=selected_hardware_type,
        node_count=optimal_node_count,
        memory_req=memory_specs,
        storage_req=storage_specs
    )
    
    return SelectHardwareInfrastructureOutput(
        hardware_infrastructure_type=selected_hardware_type,
        number_of_nodes=optimal_node_count,
        memory_required=memory_specs,
        storage_required=storage_specs,
        reasoning_description=reasoning
    )