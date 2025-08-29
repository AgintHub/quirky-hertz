from ._evaluate_model_performance.load_model_checkpoint import load_model_checkpoint
from ._evaluate_model_performance.load_code_generation_benchmark import load_code_generation_benchmark
from ._evaluate_model_performance.load_syntax_correctness_benchmark import load_syntax_correctness_benchmark
from ._evaluate_model_performance.load_code_completion_benchmark import load_code_completion_benchmark
from ._evaluate_model_performance.load_programming_language_understanding_benchmark import load_programming_language_understanding_benchmark
from ._evaluate_model_performance.run_code_generation_evaluation import run_code_generation_evaluation
from ._evaluate_model_performance.calculate_accuracy_percentage import calculate_accuracy_percentage
from ._evaluate_model_performance.run_syntax_correctness_evaluation import run_syntax_correctness_evaluation
from ._evaluate_model_performance.calculate_syntax_correctness_percentage import calculate_syntax_correctness_percentage
from ._evaluate_model_performance.run_code_completion_evaluation import run_code_completion_evaluation
from ._evaluate_model_performance.calculate_completion_accuracy_percentage import calculate_completion_accuracy_percentage
from ._evaluate_model_performance.run_language_understanding_evaluation import run_language_understanding_evaluation
from ._evaluate_model_performance.calculate_understanding_percentage import calculate_understanding_percentage
from ._evaluate_model_performance.log_evaluation_metrics import log_evaluation_metrics

from pydantic import BaseModel, Field


class TrainGpt6ModelOutput(BaseModel):
    """Pydantic model for train_gpt6_model node outputs."""
    training_metrics: str = Field(..., description="Training metrics, such as loss and accuracy, during the model training process.")
    checkpoint_status: bool = Field(..., description="Whether the model training process has reached a reasonable accuracy and is ready to be used.")
    training_time: int = Field(..., description="Total time taken to train the GPT-6 model.")


class EvaluateModelPerformanceOutput(BaseModel):
    """Pydantic model for evaluate_model_performance node outputs."""
    code_generation_accuracy: int = Field(..., description="The accuracy of code generation by the GPT-6 model.")
    syntax_correctness: int = Field(..., description="The percentage of correct syntax in the generated code by the GPT-6 model.")
    code_completion: int = Field(..., description="The accuracy of code completion by the GPT-6 model.")
    programming_language_understanding: int = Field(..., description="The understanding of programming languages by the GPT-6 model.")


def evaluate_model_performance(train_gpt6_model_input: TrainGpt6ModelOutput, **kwargs) -> EvaluateModelPerformanceOutput:
    """Assess trained model on code generation, code understanding, and language modeling benchmarks.

    Args:
        train_gpt6_model_input: Input from the 'train_gpt6_model' node.
        **kwargs: Additional keyword arguments.

    Returns:
        EvaluateModelPerformanceOutput: Object containing outputs for this node.
    """
    # Load the trained model for evaluation
    model_checkpoint = load_model_checkpoint(checkpoint_status=train_gpt6_model_input.checkpoint_status)
    
    # Prepare evaluation datasets for different benchmarks
    code_gen_dataset = load_code_generation_benchmark()
    syntax_dataset = load_syntax_correctness_benchmark()
    completion_dataset = load_code_completion_benchmark()
    language_understanding_dataset = load_programming_language_understanding_benchmark()
    
    # Evaluate code generation accuracy
    code_gen_results = run_code_generation_evaluation(model=model_checkpoint, dataset=code_gen_dataset)
    code_generation_accuracy: int = calculate_accuracy_percentage(results=code_gen_results)
    
    # Evaluate syntax correctness
    syntax_results = run_syntax_correctness_evaluation(model=model_checkpoint, dataset=syntax_dataset)
    syntax_correctness: int = calculate_syntax_correctness_percentage(results=syntax_results)
    
    # Evaluate code completion accuracy
    completion_results = run_code_completion_evaluation(model=model_checkpoint, dataset=completion_dataset)
    code_completion: int = calculate_completion_accuracy_percentage(results=completion_results)
    
    # Evaluate programming language understanding
    understanding_results = run_language_understanding_evaluation(model=model_checkpoint, dataset=language_understanding_dataset)
    programming_language_understanding: int = calculate_understanding_percentage(results=understanding_results)
    
    # Log evaluation metrics for analysis
    log_evaluation_metrics(
        training_metrics=train_gpt6_model_input.training_metrics,
        code_gen_acc=code_generation_accuracy,
        syntax_acc=syntax_correctness,
        completion_acc=code_completion,
        understanding_acc=programming_language_understanding
    )
    
    return EvaluateModelPerformanceOutput(
        code_generation_accuracy=code_generation_accuracy,
        syntax_correctness=syntax_correctness,
        code_completion=code_completion,
        programming_language_understanding=programming_language_understanding,
    )