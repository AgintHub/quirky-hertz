# -- PRD --
# 1. BULLET: Calculate the memory requirements based on the provided model size, node
#   count, and hardware type.
#   Reason: This is necessary to determine the required memory for model training.
#   Impact: The memory requirement is a critical factor in selecting the right hardware
#           setup.
#   Complexity: MEDIUM
#   Method: Use a formula or a library function to calculate the memory requirements,
#           considering factors like model size, node count, and hardware
#           type.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Validate the input parameters to ensure they are consistent with the expected
#   format.
#   Reason: Invalid input parameters can lead to incorrect memory requirements
#           calculation.
#   Impact: Validation ensures the accuracy of the output.
#   Complexity: LOW
#   Method: Use input validation libraries or custom functions to check the input
#           parameters.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Round the memory requirements to the nearest reasonable value (e.g., nearest
#   GB).
#   Reason: To simplify the output and make it easier to interpret.
#   Impact: Rounding makes the output more user-friendly.
#   Complexity: LOW
#   Method: Use rounding functions like `math.ceil()` or `round()` to round the memory
#           requirements.
# -- END PRD --


def calculate_memory_requirements(model_size: str, node_count: str, hardware_type: str) -> str:
    """
    This shim calculates the memory requirements for model training based on model size, node count, and hardware type.

    Args:
        model_size: Input parameter of type str
node_count: Input parameter of type str
hardware_type: Input parameter of type str

    Returns:
        str: Output of type str
    """
    raise NotImplementedError("This is a virtual stub node that needs to be implemented")
