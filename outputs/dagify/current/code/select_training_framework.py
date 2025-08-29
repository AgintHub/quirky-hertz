from ._select_training_framework.estimate_corpus_size import estimate_corpus_size
from ._select_training_framework.count_training_batches import count_training_batches
from ._select_training_framework.analyze_tokenization_needs import analyze_tokenization_needs
from ._select_training_framework.identify_framework_candidates import identify_framework_candidates
from ._select_training_framework.evaluate_frameworks import evaluate_frameworks
from ._select_training_framework.get_compatible_toolkits import get_compatible_toolkits
from ._select_training_framework.select_optimal_toolkit import select_optimal_toolkit
from ._select_training_framework.compile_hardware_resources import compile_hardware_resources
from ._select_training_framework.calculate_optimal_batch_size import calculate_optimal_batch_size
from ._select_training_framework.determine_learning_rate import determine_learning_rate
from ._select_training_framework.estimate_epoch_count import estimate_epoch_count
from ._select_training_framework.generate_training_plan import generate_training_plan

from pydantic import BaseModel, Field


class AssembleFullTrainingCorpusOutput(BaseModel):
    """Pydantic model for assemble_full_training_corpus node outputs."""
    unified_training_corpus: str = Field(..., description="The unified training corpus as a list of strings")
    duplicated_content_counts: int = Field(..., description="List of counts for duplicated content")
    consistent_tokenization_status: bool = Field(..., description="Whether consistent tokenization was applied successfully")
    training_batches: str = Field(..., description="List of training batches as lists of strings")


class SelectHardwareInfrastructureOutput(BaseModel):
    """Pydantic model for select_hardware_infrastructure node outputs."""
    hardware_infrastructure_type: str = Field(..., description="Type of hardware infrastructure selected (e.g., GPU, TPU, CPU)")
    number_of_nodes: int = Field(..., description="Number of nodes in the hardware infrastructure")
    memory_required: str = Field(..., description="Memory requirements of the hardware infrastructure (e.g., in GB)")
    storage_required: str = Field(..., description="Storage requirements of the hardware infrastructure (e.g., in GB)")
    reasoning_description: str = Field(..., description="Description of the reasoning behind the selected hardware infrastructure")


class SelectTrainingFrameworkOutput(BaseModel):
    """Pydantic model for select_training_framework node outputs."""
    selected_framework: str = Field(..., description="Selected machine learning framework")
    selected_toolkit: str = Field(..., description="Selected distributed training toolkit")
    hardware_resources: str = Field(..., description="List of selected hardware resources")
    training_plan: str = Field(..., description="Detailed training plan with epoch count, batch size, and learning rate")


def select_training_framework(assemble_full_training_corpus_input: AssembleFullTrainingCorpusOutput, select_hardware_infrastructure_input: SelectHardwareInfrastructureOutput, **kwargs) -> SelectTrainingFrameworkOutput:
    """Choose machine learning frameworks and distributed training tools for GPT-6 training.

    Args:
        assemble_full_training_corpus_input: Input from the 'assemble_full_training_corpus' node.
        select_hardware_infrastructure_input: Input from the 'select_hardware_infrastructure' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SelectTrainingFrameworkOutput: Object containing outputs for this node.
    """
    # Analyze corpus characteristics to determine framework requirements
    corpus_size: int = estimate_corpus_size(corpus=assemble_full_training_corpus_input.unified_training_corpus)
    batch_count: int = count_training_batches(batches=assemble_full_training_corpus_input.training_batches)
    tokenization_requirements: str = analyze_tokenization_needs(status=assemble_full_training_corpus_input.consistent_tokenization_status)
    
    # Evaluate hardware capabilities and constraints
    hardware_type: str = select_hardware_infrastructure_input.hardware_infrastructure_type
    node_count: int = select_hardware_infrastructure_input.number_of_nodes
    memory_specs: str = select_hardware_infrastructure_input.memory_required
    
    # Select optimal framework based on hardware and corpus characteristics
    framework_candidates: list = identify_framework_candidates(hardware_type=hardware_type, model_type="GPT-6")
    selected_framework: str = evaluate_frameworks(candidates=framework_candidates, corpus_size=corpus_size, hardware_specs=hardware_type)
    
    # Choose distributed training toolkit compatible with selected framework
    toolkit_options: list = get_compatible_toolkits(framework=selected_framework, node_count=node_count)
    selected_toolkit: str = select_optimal_toolkit(options=toolkit_options, hardware_type=hardware_type)
    
    # Compile hardware resources configuration
    hardware_resources: str = compile_hardware_resources(infrastructure_type=hardware_type, nodes=node_count, memory=memory_specs)
    
    # Generate detailed training plan
    optimal_batch_size: int = calculate_optimal_batch_size(corpus_size=corpus_size, hardware_memory=memory_specs)
    learning_rate: float = determine_learning_rate(framework=selected_framework, batch_size=optimal_batch_size)
    epoch_count: int = estimate_epoch_count(corpus_size=corpus_size, batch_count=batch_count)
    training_plan: str = generate_training_plan(epochs=epoch_count, batch_size=optimal_batch_size, learning_rate=learning_rate)
    
    return SelectTrainingFrameworkOutput(
        selected_framework=selected_framework,
        selected_toolkit=selected_toolkit,
        hardware_resources=hardware_resources,
        training_plan=training_plan
    )