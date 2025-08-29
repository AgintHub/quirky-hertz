from ._train_gpt6_model.validate_training_environment import validate_training_environment
from ._train_gpt6_model.setup_gpt6_training_config import setup_gpt6_training_config
from ._train_gpt6_model.load_training_corpus import load_training_corpus
from ._train_gpt6_model.initialize_gpt6_model import initialize_gpt6_model
from ._train_gpt6_model.get_current_timestamp import get_current_timestamp
from ._train_gpt6_model.execute_model_training import execute_model_training
from ._train_gpt6_model.format_training_metrics import format_training_metrics
from ._train_gpt6_model.evaluate_checkpoint_status import evaluate_checkpoint_status

from pydantic import BaseModel, Field
from typing import List


class ConfigureTrainingEnvironmentOutput(BaseModel):
    """Pydantic model for configure_training_environment node outputs."""
    environment_settings: List[str] = Field(..., description="List of environment settings, including installed libraries and dependencies.")
    containerized_environment: bool = Field(..., description="Whether the environment is containerized.")
    training_environment_status: str = Field(..., description="Status of the training environment, including any errors or warnings.")


class TrainGpt6ModelOutput(BaseModel):
    """Pydantic model for train_gpt6_model node outputs."""
    training_metrics: str = Field(..., description="Training metrics, such as loss and accuracy, during the model training process.")
    checkpoint_status: bool = Field(..., description="Whether the model training process has reached a reasonable accuracy and is ready to be used.")
    training_time: int = Field(..., description="Total time taken to train the GPT-6 model.")


def train_gpt6_model(configure_training_environment_input: ConfigureTrainingEnvironmentOutput, **kwargs) -> TrainGpt6ModelOutput:
    """Run the model training process using defined specifications and prepared corpus.

    Args:
        configure_training_environment_input: Input from the 'configure_training_environment' node.
        **kwargs: Additional keyword arguments.

    Returns:
        TrainGpt6ModelOutput: Object containing outputs for this node.
    """
    # Validate training environment is ready
    environment_ready: bool = validate_training_environment(settings=configure_training_environment_input.environment_settings, containerized=configure_training_environment_input.containerized_environment)
    
    if not environment_ready:
        return TrainGpt6ModelOutput(
            training_metrics="Training failed - environment not ready",
            checkpoint_status=False,
            training_time=0
        )
    
    # Initialize training configuration
    training_config: dict = setup_gpt6_training_config(environment_settings=configure_training_environment_input.environment_settings)
    
    # Load and prepare training data
    training_data = load_training_corpus(config=training_config)
    
    # Initialize GPT-6 model architecture
    model = initialize_gpt6_model(config=training_config)
    
    # Execute training process
    training_start_time: int = get_current_timestamp()
    training_results: dict = execute_model_training(model=model, data=training_data, config=training_config)
    training_end_time: int = get_current_timestamp()
    
    # Process training metrics
    formatted_metrics: str = format_training_metrics(results=training_results)
    
    # Evaluate checkpoint status
    checkpoint_ready: bool = evaluate_checkpoint_status(metrics=training_results, threshold_config=training_config)
    
    # Calculate total training time
    total_time: int = training_end_time - training_start_time
    
    return TrainGpt6ModelOutput(
        training_metrics=formatted_metrics,
        checkpoint_status=checkpoint_ready,
        training_time=total_time
    )