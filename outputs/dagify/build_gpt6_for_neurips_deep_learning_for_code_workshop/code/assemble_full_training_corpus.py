from ._assemble_full_training_corpus.combine_training_sources import combine_training_sources
from ._assemble_full_training_corpus.deduplicate_content import deduplicate_content
from ._assemble_full_training_corpus.count_duplicates import count_duplicates
from ._assemble_full_training_corpus.normalize_tokenization import normalize_tokenization
from ._assemble_full_training_corpus.validate_consistent_tokenization import validate_consistent_tokenization
from ._assemble_full_training_corpus.create_training_batches import create_training_batches

from pydantic import BaseModel, Field


class PrepareTrainingCorpusCodeReposOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_code_repos node outputs."""
    cleaned_repository_data: str = Field(..., description="Cleaned and formatted code repository data")
    tokenized_code: str = Field(..., description="Tokenized code data")
    training_samples: str = Field(..., description="Prepared training samples from the code repositories")


class PrepareTrainingCorpusProgrammingBooksOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_programming_books node outputs."""
    cleaned_book_content: str = Field(..., description="Preprocessed text content of programming books and documentation")
    tokenized_book_data: str = Field(..., description="List of tokenized book data after cleaning and standardizing formatting")
    structured_book_samples: str = Field(..., description="List of structured book samples suitable for training, including questions, answers, and code snippets")
    counts_of_noisy_content: int = Field(..., description="List of counts of noisy content removed during cleaning")


class PrepareTrainingCorpusStackoverflowDataOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_stackoverflow_data node outputs."""
    cleaned_posts: str = Field(..., description="List of cleaned Stack Overflow posts")
    tokenized_content: str = Field(..., description="List of tokenized content from Stack Overflow posts")
    formatted_pairs: str = Field(..., description="List of formatted paired questions and answers including code snippets")
    validation_status: bool = Field(..., description="Whether the cleaning and formatting process is valid")


class AssembleFullTrainingCorpusOutput(BaseModel):
    """Pydantic model for assemble_full_training_corpus node outputs."""
    unified_training_corpus: str = Field(..., description="The unified training corpus as a list of strings")
    duplicated_content_counts: int = Field(..., description="List of counts for duplicated content")
    consistent_tokenization_status: bool = Field(..., description="Whether consistent tokenization was applied successfully")
    training_batches: str = Field(..., description="List of training batches as lists of strings")


def assemble_full_training_corpus(prepare_training_corpus_code_repos_input: PrepareTrainingCorpusCodeReposOutput, prepare_training_corpus_programming_books_input: PrepareTrainingCorpusProgrammingBooksOutput, prepare_training_corpus_stackoverflow_data_input: PrepareTrainingCorpusStackoverflowDataOutput, **kwargs) -> AssembleFullTrainingCorpusOutput:
    """Integrate all prepared training data into a unified, deduplicated training corpus.

    Args:
        prepare_training_corpus_code_repos_input: Input from the 'prepare_training_corpus_code_repos' node.
        prepare_training_corpus_programming_books_input: Input from the 'prepare_training_corpus_programming_books' node.
        prepare_training_corpus_stackoverflow_data_input: Input from the 'prepare_training_corpus_stackoverflow_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        AssembleFullTrainingCorpusOutput: Object containing outputs for this node.
    """
    # Combine all training data sources
    combined_data: str = combine_training_sources(
        code_repos=prepare_training_corpus_code_repos_input.training_samples,
        books=prepare_training_corpus_programming_books_input.structured_book_samples,
        stackoverflow=prepare_training_corpus_stackoverflow_data_input.formatted_pairs
    )
    
    # Remove duplicates and count them
    deduplicated_corpus: str = deduplicate_content(data=combined_data)
    duplicate_counts: int = count_duplicates(original=combined_data, deduplicated=deduplicated_corpus)
    
    # Ensure consistent tokenization across all sources
    unified_corpus: str = normalize_tokenization(
        corpus=deduplicated_corpus,
        code_tokenization=prepare_training_corpus_code_repos_input.tokenized_code,
        book_tokenization=prepare_training_corpus_programming_books_input.tokenized_book_data,
        stackoverflow_tokenization=prepare_training_corpus_stackoverflow_data_input.tokenized_content
    )
    
    # Validate tokenization consistency
    tokenization_valid: bool = validate_consistent_tokenization(corpus=unified_corpus)
    
    # Create training batches
    batched_data: str = create_training_batches(corpus=unified_corpus)
    
    return AssembleFullTrainingCorpusOutput(
        unified_training_corpus=unified_corpus,
        duplicated_content_counts=duplicate_counts,
        consistent_tokenization_status=tokenization_valid,
        training_batches=batched_data
    )