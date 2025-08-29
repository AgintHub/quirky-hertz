import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.assemble_full_training_corpus import assemble_full_training_corpus
from code.collect_open_source_code_repositories import collect_open_source_code_repositories
from code.collect_programming_books_text import collect_programming_books_text
from code.collect_stackoverflow_and_forum_data import collect_stackoverflow_and_forum_data
from code.configure_training_environment import configure_training_environment
from code.define_model_specifications import define_model_specifications
from code.evaluate_model_performance import evaluate_model_performance
from code.prepare_training_corpus_code_repos import prepare_training_corpus_code_repos
from code.prepare_training_corpus_programming_books import prepare_training_corpus_programming_books
from code.prepare_training_corpus_stackoverflow_data import prepare_training_corpus_stackoverflow_data
from code.prepare_workshop_presentation_materials import prepare_workshop_presentation_materials
from code.select_hardware_infrastructure import select_hardware_infrastructure
from code.select_training_framework import select_training_framework
from code.train_gpt6_model import train_gpt6_model

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

assemble_full_training_corpus_async = make_async(assemble_full_training_corpus)
collect_open_source_code_repositories_async = make_async(collect_open_source_code_repositories)
collect_programming_books_text_async = make_async(collect_programming_books_text)
collect_stackoverflow_and_forum_data_async = make_async(collect_stackoverflow_and_forum_data)
configure_training_environment_async = make_async(configure_training_environment)
define_model_specifications_async = make_async(define_model_specifications)
evaluate_model_performance_async = make_async(evaluate_model_performance)
prepare_training_corpus_code_repos_async = make_async(prepare_training_corpus_code_repos)
prepare_training_corpus_programming_books_async = make_async(prepare_training_corpus_programming_books)
prepare_training_corpus_stackoverflow_data_async = make_async(prepare_training_corpus_stackoverflow_data)
prepare_workshop_presentation_materials_async = make_async(prepare_workshop_presentation_materials)
select_hardware_infrastructure_async = make_async(select_hardware_infrastructure)
select_training_framework_async = make_async(select_training_framework)
train_gpt6_model_async = make_async(train_gpt6_model)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: collect_stackoverflow_and_forum_data, collect_open_source_code_repositories, define_model_specifications, collect_programming_books_text
    async def run_collect_stackoverflow_and_forum_data():
        # Call the async version of collect_stackoverflow_and_forum_data with results from dependencies
        return await collect_stackoverflow_and_forum_data_async(user_input)

    async def run_collect_open_source_code_repositories():
        # Call the async version of collect_open_source_code_repositories with results from dependencies
        return await collect_open_source_code_repositories_async(user_input)

    async def run_define_model_specifications():
        # Call the async version of define_model_specifications with results from dependencies
        return await define_model_specifications_async(user_input)

    async def run_collect_programming_books_text():
        # Call the async version of collect_programming_books_text with results from dependencies
        return await collect_programming_books_text_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_collect_stackoverflow_and_forum_data(), run_collect_open_source_code_repositories(), run_define_model_specifications(), run_collect_programming_books_text())
    results['collect_stackoverflow_and_forum_data'] = level_0_results[0]
    results['collect_open_source_code_repositories'] = level_0_results[1]
    results['define_model_specifications'] = level_0_results[2]
    results['collect_programming_books_text'] = level_0_results[3]

    # Level 1: select_hardware_infrastructure, prepare_training_corpus_stackoverflow_data, prepare_training_corpus_code_repos, prepare_training_corpus_programming_books
    async def run_select_hardware_infrastructure():
        # Call the async version of select_hardware_infrastructure with results from dependencies
        return await select_hardware_infrastructure_async(results['define_model_specifications'])

    async def run_prepare_training_corpus_stackoverflow_data():
        # Call the async version of prepare_training_corpus_stackoverflow_data with results from dependencies
        return await prepare_training_corpus_stackoverflow_data_async(results['collect_stackoverflow_and_forum_data'])

    async def run_prepare_training_corpus_code_repos():
        # Call the async version of prepare_training_corpus_code_repos with results from dependencies
        return await prepare_training_corpus_code_repos_async(results['collect_open_source_code_repositories'])

    async def run_prepare_training_corpus_programming_books():
        # Call the async version of prepare_training_corpus_programming_books with results from dependencies
        return await prepare_training_corpus_programming_books_async(results['collect_programming_books_text'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_select_hardware_infrastructure(), run_prepare_training_corpus_stackoverflow_data(), run_prepare_training_corpus_code_repos(), run_prepare_training_corpus_programming_books())
    results['select_hardware_infrastructure'] = level_1_results[0]
    results['prepare_training_corpus_stackoverflow_data'] = level_1_results[1]
    results['prepare_training_corpus_code_repos'] = level_1_results[2]
    results['prepare_training_corpus_programming_books'] = level_1_results[3]

    # Level 2: assemble_full_training_corpus
    async def run_assemble_full_training_corpus():
        # Call the async version of assemble_full_training_corpus with results from dependencies
        return await assemble_full_training_corpus_async(results['prepare_training_corpus_code_repos'], results['prepare_training_corpus_programming_books'], results['prepare_training_corpus_stackoverflow_data'])

    # Run level 2 nodes in parallel
    results['assemble_full_training_corpus'] = await run_assemble_full_training_corpus()

    # Level 3: select_training_framework
    async def run_select_training_framework():
        # Call the async version of select_training_framework with results from dependencies
        return await select_training_framework_async(results['assemble_full_training_corpus'], results['select_hardware_infrastructure'])

    # Run level 3 nodes in parallel
    results['select_training_framework'] = await run_select_training_framework()

    # Level 4: configure_training_environment
    async def run_configure_training_environment():
        # Call the async version of configure_training_environment with results from dependencies
        return await configure_training_environment_async(results['select_training_framework'])

    # Run level 4 nodes in parallel
    results['configure_training_environment'] = await run_configure_training_environment()

    # Level 5: train_gpt6_model
    async def run_train_gpt6_model():
        # Call the async version of train_gpt6_model with results from dependencies
        return await train_gpt6_model_async(results['configure_training_environment'])

    # Run level 5 nodes in parallel
    results['train_gpt6_model'] = await run_train_gpt6_model()

    # Level 6: evaluate_model_performance
    async def run_evaluate_model_performance():
        # Call the async version of evaluate_model_performance with results from dependencies
        return await evaluate_model_performance_async(results['train_gpt6_model'])

    # Run level 6 nodes in parallel
    results['evaluate_model_performance'] = await run_evaluate_model_performance()

    # Level 7: prepare_workshop_presentation_materials
    async def run_prepare_workshop_presentation_materials():
        # Call the async version of prepare_workshop_presentation_materials with results from dependencies
        return await prepare_workshop_presentation_materials_async(results['evaluate_model_performance'])

    # Run level 7 nodes in parallel
    results['prepare_workshop_presentation_materials'] = await run_prepare_workshop_presentation_materials()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
