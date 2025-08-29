from ._prepare_training_corpus_code_repos.download_repository_contents import download_repository_contents
from ._prepare_training_corpus_code_repos.filter_code_files import filter_code_files
from ._prepare_training_corpus_code_repos.clean_code_data import clean_code_data
from ._prepare_training_corpus_code_repos.tokenize_code_content import tokenize_code_content
from ._prepare_training_corpus_code_repos.format_training_samples import format_training_samples

from pydantic import BaseModel, Field
from typing import List


class CollectOpenSourceCodeRepositoriesOutput(BaseModel):
    """Pydantic model for collect_open_source_code_repositories node outputs."""
    repository_list: List[str] = Field(..., description="List of open-source code repository URLs")
    language_distribution: List[str] = Field(..., description="List of programming languages with their respective repository counts")
    repository_metadata: List[str] = Field(..., description="List of repository metadata (language, size, domain)")


class PrepareTrainingCorpusCodeReposOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_code_repos node outputs."""
    cleaned_repository_data: str = Field(..., description="Cleaned and formatted code repository data")
    tokenized_code: str = Field(..., description="Tokenized code data")
    training_samples: str = Field(..., description="Prepared training samples from the code repositories")


def prepare_training_corpus_code_repos(collect_open_source_code_repositories_input: CollectOpenSourceCodeRepositoriesOutput, **kwargs) -> PrepareTrainingCorpusCodeReposOutput:
    """Clean, tokenize, and format open-source code repositories for model ingestion.

    Args:
        collect_open_source_code_repositories_input: Input from the 'collect_open_source_code_repositories' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PrepareTrainingCorpusCodeReposOutput: Object containing outputs for this node.
    """
    # Extract repository data from input
    repositories: List[str] = collect_open_source_code_repositories_input.repository_list
    metadata: List[str] = collect_open_source_code_repositories_input.repository_metadata
    
    # Download and extract code content from repositories
    raw_code_content: str = download_repository_contents(repositories=repositories)
    
    # Clean and preprocess the code data
    filtered_code: str = filter_code_files(raw_content=raw_code_content, metadata=metadata)
    cleaned_data: str = clean_code_data(code_content=filtered_code)
    
    # Tokenize the cleaned code
    tokenized_result: str = tokenize_code_content(cleaned_code=cleaned_data)
    
    # Prepare training samples with appropriate formatting
    formatted_samples: str = format_training_samples(tokenized_data=tokenized_result, metadata=metadata)
    
    return PrepareTrainingCorpusCodeReposOutput(
        cleaned_repository_data=cleaned_data,
        tokenized_code=tokenized_result,
        training_samples=formatted_samples
    )