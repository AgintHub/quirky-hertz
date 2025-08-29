from ._prepare_training_corpus_stackoverflow_data.clean_stackoverflow_posts import clean_stackoverflow_posts
from ._prepare_training_corpus_stackoverflow_data.clean_text_content import clean_text_content
from ._prepare_training_corpus_stackoverflow_data.clean_code_snippets import clean_code_snippets
from ._prepare_training_corpus_stackoverflow_data.tokenize_content import tokenize_content
from ._prepare_training_corpus_stackoverflow_data.tokenize_code_content import tokenize_code_content
from ._prepare_training_corpus_stackoverflow_data.combine_tokenized_content import combine_tokenized_content
from ._prepare_training_corpus_stackoverflow_data.format_qa_pairs_with_code import format_qa_pairs_with_code
from ._prepare_training_corpus_stackoverflow_data.validate_training_corpus import validate_training_corpus

from pydantic import BaseModel, Field


class CollectStackoverflowAndForumDataOutput(BaseModel):
    """Pydantic model for collect_stackoverflow_and_forum_data node outputs."""
    stackoverflow_posts: str = Field(..., description="List of Stack Overflow post titles and texts")
    forum_discussions: str = Field(..., description="List of Q&A forum discussion titles and texts")
    questions: str = Field(..., description="List of question texts")
    answers: str = Field(..., description="List of answer texts")
    code_snippets: str = Field(..., description="List of code snippets")


class PrepareTrainingCorpusStackoverflowDataOutput(BaseModel):
    """Pydantic model for prepare_training_corpus_stackoverflow_data node outputs."""
    cleaned_posts: str = Field(..., description="List of cleaned Stack Overflow posts")
    tokenized_content: str = Field(..., description="List of tokenized content from Stack Overflow posts")
    formatted_pairs: str = Field(..., description="List of formatted paired questions and answers including code snippets")
    validation_status: bool = Field(..., description="Whether the cleaning and formatting process is valid")


def prepare_training_corpus_stackoverflow_data(collect_stackoverflow_and_forum_data_input: CollectStackoverflowAndForumDataOutput, **kwargs) -> PrepareTrainingCorpusStackoverflowDataOutput:
    """Clean, tokenize, and convert Stack Overflow and forum data into training samples.

    Args:
        collect_stackoverflow_and_forum_data_input: Input from the 'collect_stackoverflow_and_forum_data' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PrepareTrainingCorpusStackoverflowDataOutput: Object containing outputs for this node.
    """
    # Clean the raw posts and forum discussions
    cleaned_stackoverflow_posts: str = clean_stackoverflow_posts(
        posts=collect_stackoverflow_and_forum_data_input.stackoverflow_posts,
        discussions=collect_stackoverflow_and_forum_data_input.forum_discussions
    )
    
    # Clean questions and answers separately
    cleaned_questions: str = clean_text_content(
        content=collect_stackoverflow_and_forum_data_input.questions
    )
    cleaned_answers: str = clean_text_content(
        content=collect_stackoverflow_and_forum_data_input.answers
    )
    
    # Process and clean code snippets
    cleaned_code_snippets: str = clean_code_snippets(
        code_snippets=collect_stackoverflow_and_forum_data_input.code_snippets
    )
    
    # Tokenize all cleaned content
    tokenized_posts: str = tokenize_content(content=cleaned_stackoverflow_posts)
    tokenized_qa: str = tokenize_content(content=cleaned_questions + cleaned_answers)
    tokenized_code: str = tokenize_code_content(content=cleaned_code_snippets)
    
    # Combine all tokenized content
    combined_tokenized_content: str = combine_tokenized_content(
        posts=tokenized_posts,
        qa_content=tokenized_qa,
        code_content=tokenized_code
    )
    
    # Format question-answer pairs with code snippets for training
    formatted_training_pairs: str = format_qa_pairs_with_code(
        questions=cleaned_questions,
        answers=cleaned_answers,
        code_snippets=cleaned_code_snippets
    )
    
    # Validate the cleaning and formatting process
    validation_result: bool = validate_training_corpus(
        cleaned_posts=cleaned_stackoverflow_posts,
        tokenized_content=combined_tokenized_content,
        formatted_pairs=formatted_training_pairs
    )
    
    return PrepareTrainingCorpusStackoverflowDataOutput(
        cleaned_posts=cleaned_stackoverflow_posts,
        tokenized_content=combined_tokenized_content,
        formatted_pairs=formatted_training_pairs,
        validation_status=validation_result
    )