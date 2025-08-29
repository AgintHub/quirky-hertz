from ._prepare_workshop_presentation_materials.parse_evaluation_metrics import parse_evaluation_metrics
from ._prepare_workshop_presentation_materials.create_architecture_slides import create_architecture_slides
from ._prepare_workshop_presentation_materials.create_training_pipeline_slides import create_training_pipeline_slides
from ._prepare_workshop_presentation_materials.extract_dataset_information import extract_dataset_information
from ._prepare_workshop_presentation_materials.create_benchmark_slides import create_benchmark_slides
from ._prepare_workshop_presentation_materials.create_implications_slides import create_implications_slides
from ._prepare_workshop_presentation_materials.create_demo_scripts import create_demo_scripts
from ._prepare_workshop_presentation_materials.combine_presentation_materials import combine_presentation_materials
from ._prepare_workshop_presentation_materials.generate_slide_title import generate_slide_title
from ._prepare_workshop_presentation_materials.format_benchmark_summary import format_benchmark_summary

from pydantic import BaseModel, Field


# -- PRD --
# 1. BULLET: Parse the output of the evaluate_model_performance node to extract relevant
#   metrics and results.
#   Reason: This is necessary to create accurate and comprehensive presentation
#           materials.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use a combination of regular expressions and custom parsing functions to
#           extract the desired information from the output data.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create a series of slides that cover GPT-6 architecture, training pipeline,
#   datasets used, benchmark results, and implications for code AI.
#   Reason: This is necessary to provide a clear and concise overview of the GPT-6
#           model's capabilities and limitations.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use a presentation software such as PowerPoint or Google Slides to create
#           the slides, and incorporate images, charts, and other visual
#           aids to make the presentation more engaging.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Develop live demo scripts that demonstrate the capabilities of the GPT-6
#   model.
#   Reason: This is necessary to provide a hands-on experience for the workshop
#           attendees and showcase the model's capabilities.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use a programming language such as Python to create the demo scripts, and
#           utilize libraries such as PyTorch or TensorFlow to interact
#           with the GPT-6 model.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Combine the slides and demo scripts into a single presentation document.
#   Reason: This is necessary to provide a cohesive and easy-to-follow presentation.
#   Impact: MEDIUM
#   Complexity: LOW
#   Method: Use a presentation software such as PowerPoint or Google Slides to combine
#           the slides and demo scripts, and make sure to include a table
#           of contents and page numbers.
# -- END PRD --



class EvaluateModelPerformanceOutput(BaseModel):
    """Pydantic model for evaluate_model_performance node outputs."""
    code_generation_accuracy: int = Field(..., description="The accuracy of code generation by the GPT-6 model.")
    syntax_correctness: int = Field(..., description="The percentage of correct syntax in the generated code by the GPT-6 model.")
    code_completion: int = Field(..., description="The accuracy of code completion by the GPT-6 model.")
    programming_language_understanding: int = Field(..., description="The understanding of programming languages by the GPT-6 model.")


class PrepareWorkshopPresentationMaterialsOutput(BaseModel):
    """Pydantic model for prepare_workshop_presentation_materials node outputs."""
    workshop_slide_title: str = Field(..., description="The title of the slide covering GPT-6 architecture.")
    dataset_used: str = Field(..., description="The name of the dataset used for training the GPT-6 model.")
    benchmark_results: str = Field(..., description="A summary of the benchmark results, including code generation accuracy and syntax correctness.")
    presentation_materials: str = Field(..., description="The final presentation materials, including slides and live demo scripts.")


def prepare_workshop_presentation_materials(evaluate_model_performance_input: EvaluateModelPerformanceOutput, **kwargs) -> PrepareWorkshopPresentationMaterialsOutput:
    """Create slides, demos, and documentation explaining GPT-6 design, training, and benchmark results for the workshop.

    Args:
        evaluate_model_performance_input: Input from the 'evaluate_model_performance' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PrepareWorkshopPresentationMaterialsOutput: Object containing outputs for this node.
    """
    # Parse and extract metrics from evaluation results
    parsed_metrics: dict = parse_evaluation_metrics(
        code_gen_accuracy=evaluate_model_performance_input.code_generation_accuracy,
        syntax_correctness=evaluate_model_performance_input.syntax_correctness,
        code_completion=evaluate_model_performance_input.code_completion,
        lang_understanding=evaluate_model_performance_input.programming_language_understanding
    )
    
    # Create architecture slides covering GPT-6 design
    architecture_slides: str = create_architecture_slides(model_name="GPT-6")
    
    # Generate training pipeline documentation
    training_slides: str = create_training_pipeline_slides()
    
    # Extract dataset information for presentation
    dataset_info: str = extract_dataset_information()
    
    # Create benchmark results visualization
    benchmark_slides: str = create_benchmark_slides(metrics=parsed_metrics)
    
    # Generate implications analysis for code AI
    implications_slides: str = create_implications_slides(metrics=parsed_metrics)
    
    # Develop live demo scripts
    demo_scripts: str = create_demo_scripts(model="GPT-6")
    
    # Combine all materials into final presentation
    final_presentation: str = combine_presentation_materials(
        architecture=architecture_slides,
        training=training_slides,
        benchmarks=benchmark_slides,
        implications=implications_slides,
        demos=demo_scripts
    )
    
    # Generate slide title
    slide_title: str = generate_slide_title(topic="GPT-6 Architecture")
    
    # Format benchmark summary
    benchmark_summary: str = format_benchmark_summary(metrics=parsed_metrics)
    
    return PrepareWorkshopPresentationMaterialsOutput(
        workshop_slide_title=slide_title,
        dataset_used=dataset_info,
        benchmark_results=benchmark_summary,
        presentation_materials=final_presentation
    )