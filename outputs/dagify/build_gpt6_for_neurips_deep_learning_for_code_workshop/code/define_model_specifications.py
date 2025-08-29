from ._define_model_specifications.analyze_code_task_requirements import analyze_code_task_requirements
from ._define_model_specifications.generate_model_name import generate_model_name
from ._define_model_specifications.calculate_optimal_model_size import calculate_optimal_model_size
from ._define_model_specifications.determine_model_modality import determine_model_modality
from ._define_model_specifications.design_code_optimized_architecture import design_code_optimized_architecture
from ._define_model_specifications.define_code_capabilities import define_code_capabilities

from pydantic import BaseModel, Field


class DefineModelSpecificationsOutput(BaseModel):
    """Pydantic model for define_model_specifications node outputs."""
    model_name: str = Field(..., description="Name of the GPT-6 model")
    model_size: int = Field(..., description="Number of parameters in the GPT-6 model")
    model_modality: str = Field(..., description="Type of input data for the GPT-6 model (e.g., text, code)")
    model_architecture: str = Field(..., description="Architecture of the GPT-6 model")
    expected_capabilities: str = Field(..., description="Expected capabilities of the GPT-6 model for deep learning with code")


def define_model_specifications(general_input: str, **kwargs) -> DefineModelSpecificationsOutput:
    """Specify GPT-6 architecture, size, modality, and design goals tailored for code tasks.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineModelSpecificationsOutput: Object containing outputs for this node.
    """
    # Analyze requirements and determine optimal model specifications
    requirements_analysis: dict = analyze_code_task_requirements(input_description=general_input, **kwargs)
    
    # Define model name based on specifications and capabilities
    model_name: str = generate_model_name(task_type="code", version="gpt-6", analysis=requirements_analysis)
    
    # Determine optimal model size for code tasks
    model_size: int = calculate_optimal_model_size(task_requirements=requirements_analysis, target_modality="code")
    
    # Specify input modality for code-focused tasks
    model_modality: str = determine_model_modality(requirements=requirements_analysis, primary_focus="code")
    
    # Design architecture optimized for code understanding and generation
    model_architecture: str = design_code_optimized_architecture(size=model_size, modality=model_modality, requirements=requirements_analysis)
    
    # Define expected capabilities for deep learning with code
    expected_capabilities: str = define_code_capabilities(architecture=model_architecture, size=model_size, requirements=requirements_analysis)
    
    return DefineModelSpecificationsOutput(
        model_name=model_name,
        model_size=model_size,
        model_modality=model_modality,
        model_architecture=model_architecture,
        expected_capabilities=expected_capabilities
    )