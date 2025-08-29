from ._prepare_training_corpus_programming_books.clean_programming_book_content import clean_programming_book_content
from ._prepare_training_corpus_programming_books.count_removed_noisy_content import count_removed_noisy_content
from ._prepare_training_corpus_programming_books.tokenize_programming_content import tokenize_programming_content
from ._prepare_training_corpus_programming_books.create_structured_training_samples import create_structured_training_samples

from pydantic import BaseModel, Field


class CollectProgrammingBooksTextOutput(BaseModel):
    """Pydantic model for collect_programming_books_text node outputs."""
    programming_book_texts: str = Field(..., description="The texts or extracts from programming books, tutorials, and official documentation")
    programming_languages: str = Field(..., description="The list of programming languages tagged in the texts")
    covered_subjects: str = Field(..., description="The list of subjects or topics covered in the texts")


class PrepareTrainingCorpusProgrammingBooksOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_programming_books node outputs."""
    cleaned_book_content: str = Field(..., description="Preprocessed text content of programming books and documentation")
    tokenized_book_data: str = Field(..., description="List of tokenized book data after cleaning and standardizing formatting")
    structured_book_samples: str = Field(..., description="List of structured book samples suitable for training, including questions, answers, and code snippets")
    counts_of_noisy_content: int = Field(..., description="List of counts of noisy content removed during cleaning")


def prepare_training_corpus_programming_books(collect_programming_books_text_input: CollectProgrammingBooksTextOutput, **kwargs) -> PrepareTrainingCorpusProgrammingBooksOutput:
    """Clean, tokenize, and format programming books and documentation into training data.

    Args:
        collect_programming_books_text_input: Input from the 'collect_programming_books_text' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PrepareTrainingCorpusProgrammingBooksOutput: Object containing outputs for this node.
    """
    # Clean the raw programming book texts
    cleaned_content: str = clean_programming_book_content(
        raw_texts=collect_programming_books_text_input.programming_book_texts,
        languages=collect_programming_books_text_input.programming_languages
    )
    
    # Count noisy content removed during cleaning
    noise_count: int = count_removed_noisy_content(
        original_texts=collect_programming_books_text_input.programming_book_texts,
        cleaned_texts=cleaned_content
    )
    
    # Tokenize the cleaned content
    tokenized_data: str = tokenize_programming_content(
        cleaned_content=cleaned_content,
        programming_languages=collect_programming_books_text_input.programming_languages
    )
    
    # Structure the content into training samples
    structured_samples: str = create_structured_training_samples(
        tokenized_data=tokenized_data,
        covered_subjects=collect_programming_books_text_input.covered_subjects,
        programming_languages=collect_programming_books_text_input.programming_languages
    )
    
    return PrepareTrainingCorpusProgrammingBooksOutput(
        cleaned_book_content=cleaned_content,
        tokenized_book_data=tokenized_data,
        structured_book_samples=structured_samples,
        counts_of_noisy_content=noise_count
    )