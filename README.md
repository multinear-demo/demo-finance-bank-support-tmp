# Demo Bank Customer Support

This is a simple Retrieval-Augmented Generation (RAG) demo tailored for a bank's customer support bot.

<!-- ## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [Experimentation Platform](#experimentation-platform)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license) -->

## Introduction

<img align="right" width="400" src="static/screenshot.png">

- This project serves as a proof-of-concept for integrating RAG into a banking environment to enhance customer support operations. By leveraging GenAI, the system provides intelligent and contextually relevant responses to customer inquiries, ensuring a seamless and efficient support experience.

- This project is also a demonstration of a platform that facilitates the development of GenAI-based applications. It allows practitioners to run various experimental configurations, measure their outcomes, and iteratively improve the system's performance while maintaining reliability and security.

### Features

- **Retrieval-Augmented Generation (RAG):** Combines traditional information retrieval methods with generative AI to provide accurate and context-aware responses.
- **Experiment Management:** Run multiple variations of the RAG engine, each with different models, prompts, or approaches.
- **Comprehensive Evaluations:** Supports various evaluation methods, including automated metrics, LLM-as-a-judge, and human evaluations.
- **Result Tracking and Comparison:** Save metadata and results of each experiment batch, enabling detailed comparisons and analysis.
- **Security and Guardrails:** Implement tests for malicious inputs and enforce security measures to safeguard against potential threats.
- **User-Friendly Interface:** A frontend interface for interacting with the customer support bot and managing experiments.


## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/multinear-demo/demo-bank-support-li-py
    cd demo-bank-support-li-py
    ```

2. **Configure Environment Variables**

   Create a `.env` file in the root directory and add your OpenAI API key:

    ```bash
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    ```

### Option 1: Using `uv` (Recommended)

[`uv`](https://github.com/astral-sh/uv) is an efficient way to run the application with minimal setup.

#### Setup Environment

```bash
uv sync
```

#### Start the Application

```bash
uv run main.py
```

### Option 2: Using `pyenv` (Alternative)

[`pyenv`](https://github.com/pyenv/pyenv) allows you to manage multiple Python versions and virtual environments seamlessly.

#### Setup Environment

```bash
pyenv install 3.9
pyenv virtualenv 3.9 demo-bank
pyenv activate demo-bank
pip install -r requirements.txt
```

#### Start the Application

```bash
python main.py
```

### Option 3: Using Python's Built-in `venv` (Another alternative)

#### Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows:
# .\.venv\Scripts\activate
pip install -r requirements.txt
```

#### Start the Application

```bash
python main.py
```

---

### Jupyter Notebook

```bash
uv run --with jupyter jupyter lab notebook.ipynb
```

or (with `pyenv` / `virtualenv`)

```bash
jupyter lab notebook.ipynb
```


## Architecture

The system is composed of several key components:

1. **RAG Engine (`engine/engine.py`):** Handles document ingestion, indexing, and query processing using the `llama_index` library and OpenAI's GPT models.
2. **API Server (`main.py`):** Built with FastAPI, it serves as the backend, exposing endpoints for chat interactions, index refreshing, and session management.
3. **Frontend (`static/index.html` & `static/app.js`):** A React-based user interface that allows users to interact with the customer support bot and manage chat sessions.
4. **Experiment Runner (`.multinear/task_runner.py`):** Facilitates running multiple experimental tasks, managing the execution of different RAG engine configurations.
5. **Configuration and Data (`.multinear/config.yaml` & `data/acme_bank_faq.txt`):** Defines experimental tasks and provides the dataset for the RAG engine.

## Experimentation Platform

The platform is designed to facilitate the development and evaluation of GenAI applications through systematic experimentation.

### Running Experiments

1. **Define Tasks**

   Configure your experimental tasks in `.multinear/config.yaml`. Each task represents a specific input scenario for the customer support bot.

2. **Execute Experiments**

Use the task runner to execute various configurations of the RAG engine. Each run can vary models, prompts, datasets, or other parameters influencing the system's behavior.

```bash
multinear run
```

3. **Monitor Execution**

   The platform will display real-time updates on the status of each task, including successes and failures.

### Evaluating Results

1. **Review Batch Runs**

   After experiment execution, access the results to compare different runs. Evaluate metrics such as response accuracy, relevance, and compliance with security standards.

2. **Analyze Metadata**

   Examine metadata associated with each run to understand the conditions and configurations that led to specific outcomes.

3. **Identify Improvements and Regressions**

   Determine which configurations enhanced performance and identify any regressions in previously working cases.

4. **Iterate for Reliability**

   Use insights from evaluations to iterate on your approach, ensuring the end-to-end system remains reliable despite the inherent unpredictability of GenAI models.

## Testing and Security

Building reliable GenAI systems involves rigorous testing to ensure robustness against various challenges.

- **Malicious Input Testing:** Validate the system's resilience against attempts to exploit vulnerabilities through crafted inputs.
- **Security Guardrails:** Implement measures to protect sensitive data and maintain compliance with regulatory standards.
- **Continuous Monitoring:** Regularly assess system performance and security postures to preemptively address potential issues.

## Project Structure


- **engine/**: Contains the RAG engine implementation.
- **static/**: Hosts the frontend HTML and JavaScript files.
- **data/**: Includes datasets used by the RAG engine for document retrieval.
- **.multinear/**: Configuration and logs for the experimentation platform.
- **main.py**: The FastAPI backend server.
- **requirements.txt & pyproject.toml**: Define project dependencies.
- **notebook.ipynb**: Jupyter notebook for interactive experimentation and testing.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes with clear commit messages.
4. Submit a pull request to the `main` branch.

Please ensure that your code adheres to the project's coding standards.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Built by [Multinear](https://multinear.com). For more information, visit our [documentation](https://multinear.com/docs/).*


# setup + run
recommended: install uv
uv sync
uv run main.py

alternative: pyenv
pyenv install
pyenv activate

less recommended: whatever python is installed

then:
pip install -r requirements.txt
python main.py

---

uv run --with jupyter jupyter lab notebook.ipynb
