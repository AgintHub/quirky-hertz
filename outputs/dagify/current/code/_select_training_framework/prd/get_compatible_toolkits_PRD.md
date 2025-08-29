# get_compatible_toolkits PRD

## Description
Selects and returns a list of distributed training toolkits compatible with the selected ML framework and node count.


## Implementation Plan

### 1. Integrate a framework agnostic toolkit database to store and retrieve compatible distributed training toolkits.

| Category | Details |
| --- | --- |
| **Reason** | To ensure accuracy and scalability of the toolkit selection process. |
| **Impact** | This change will enable the selection of compatible toolkits based on the framework and node count. |
| **Complexity** | MEDIUM |
| **Method** | Implement a SQL or NoSQL database to store toolkit metadata, and design API endpoints for retrieval and filtering. |

### 2. Develop an algorithm to filter and rank the compatible toolkits based on their compatibility with the selected framework and node count.

| Category | Details |
| --- | --- |
| **Reason** | To provide a relevant and manageable list of compatible toolkits to the user. |
| **Impact** | This change will improve the user experience by providing a curated list of toolkits that meet their requirements. |
| **Complexity** | MEDIUM |
| **Method** | Implement a ranking algorithm that takes into account factors such as toolkit version, framework version, and node count compatibility. |
