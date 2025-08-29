from ._collect_open_source_code_repositories.parse_collection_criteria import parse_collection_criteria
from ._collect_open_source_code_repositories.search_github_repositories import search_github_repositories
from ._collect_open_source_code_repositories.search_gitlab_repositories import search_gitlab_repositories
from ._collect_open_source_code_repositories.search_other_code_platforms import search_other_code_platforms
from ._collect_open_source_code_repositories.merge_and_deduplicate_repos import merge_and_deduplicate_repos
from ._collect_open_source_code_repositories.filter_repositories_by_quality import filter_repositories_by_quality
from ._collect_open_source_code_repositories.analyze_repository_languages import analyze_repository_languages
from ._collect_open_source_code_repositories.format_language_distribution import format_language_distribution
from ._collect_open_source_code_repositories.extract_repository_metadata import extract_repository_metadata
from ._collect_open_source_code_repositories.format_repository_metadata import format_repository_metadata
from ._collect_open_source_code_repositories.ensure_repository_diversity import ensure_repository_diversity

from pydantic import BaseModel, Field
from typing import List


class CollectOpenSourceCodeRepositoriesOutput(BaseModel):
    """Pydantic model for collect_open_source_code_repositories node outputs."""
    repository_list: List[str] = Field(..., description="List of open-source code repository URLs")
    language_distribution: List[str] = Field(..., description="List of programming languages with their respective repository counts")
    repository_metadata: List[str] = Field(..., description="List of repository metadata (language, size, domain)")


def collect_open_source_code_repositories(general_input: str, **kwargs) -> CollectOpenSourceCodeRepositoriesOutput:
    """Gather a diverse set of open-source code repositories for training.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        CollectOpenSourceCodeRepositoriesOutput: Object containing outputs for this node.
    """
    # Parse input parameters and configuration
    search_criteria: dict = parse_collection_criteria(input_text=general_input, kwargs=kwargs)
    
    # Discover repositories from multiple sources
    github_repos: List[str] = search_github_repositories(criteria=search_criteria)
    gitlab_repos: List[str] = search_gitlab_repositories(criteria=search_criteria)
    other_repos: List[str] = search_other_code_platforms(criteria=search_criteria)
    
    # Combine and deduplicate repository lists
    all_repositories: List[str] = merge_and_deduplicate_repos(github_repos=github_repos, gitlab_repos=gitlab_repos, other_repos=other_repos)
    
    # Filter repositories based on quality and relevance
    filtered_repos: List[str] = filter_repositories_by_quality(repositories=all_repositories, criteria=search_criteria)
    
    # Analyze programming languages across repositories
    language_stats: dict = analyze_repository_languages(repositories=filtered_repos)
    language_distribution_formatted: List[str] = format_language_distribution(language_stats=language_stats)
    
    # Extract metadata for each repository
    repository_metadata_raw: List[dict] = extract_repository_metadata(repositories=filtered_repos)
    repository_metadata_formatted: List[str] = format_repository_metadata(metadata=repository_metadata_raw)
    
    # Validate and ensure diversity in the final collection
    final_repo_list: List[str] = ensure_repository_diversity(repositories=filtered_repos, language_stats=language_stats)
    
    return CollectOpenSourceCodeRepositoriesOutput(
        repository_list=final_repo_list,
        language_distribution=language_distribution_formatted,
        repository_metadata=repository_metadata_formatted
    )