from ._collect_programming_books_text.identify_programming_book_sources import identify_programming_book_sources
from ._collect_programming_books_text.extract_text_from_sources import extract_text_from_sources
from ._collect_programming_books_text.preprocess_programming_texts import preprocess_programming_texts
from ._collect_programming_books_text.detect_programming_languages import detect_programming_languages
from ._collect_programming_books_text.extract_covered_topics import extract_covered_topics
from ._collect_programming_books_text.format_training_corpus import format_training_corpus

from pydantic import BaseModel, Field


class CollectProgrammingBooksTextOutput(BaseModel):
    """Pydantic model for collect_programming_books_text node outputs."""
    programming_book_texts: str = Field(..., description="The texts or extracts from programming books, tutorials, and official documentation")
    programming_languages: str = Field(..., description="The list of programming languages tagged in the texts")
    covered_subjects: str = Field(..., description="The list of subjects or topics covered in the texts")


def collect_programming_books_text(general_input: str, **kwargs) -> CollectProgrammingBooksTextOutput:
    """Acquire text corpora of programming books and documentation for training

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        CollectProgrammingBooksTextOutput: Object containing outputs for this node.
    """
    # Identify and gather programming book sources
    book_sources: list = identify_programming_book_sources(input_query=general_input)
    
    # Collect raw text content from various sources
    raw_book_texts: str = extract_text_from_sources(sources=book_sources)
    
    # Clean and preprocess the collected texts
    cleaned_texts: str = preprocess_programming_texts(raw_text=raw_book_texts)
    
    # Analyze and extract programming languages mentioned
    detected_languages: str = detect_programming_languages(text_content=cleaned_texts)
    
    # Identify subjects and topics covered in the texts
    extracted_subjects: str = extract_covered_topics(text_content=cleaned_texts)
    
    # Format and structure the final text corpus
    formatted_texts: str = format_training_corpus(processed_text=cleaned_texts)
    
    return CollectProgrammingBooksTextOutput(
        programming_book_texts=formatted_texts,
        programming_languages=detected_languages,
        covered_subjects=extracted_subjects
    )