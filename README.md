# Hence - A minimal python workflow engine

## Introduction

Welcome to Hence, a powerful framework designed to streamline your workflow orchestration process. Whether you're involved in web scraping, data loading, fetching, or any other repetitive task, Hence offers a comprehensive solution to break down these tasks into manageable units of work. By orchestrating these units sequentially, Hence empowers you to focus on the big picture without the hassle of manually ensuring the success of each step.

## Features and Use-cases

Read [Features and Use-cases](./docs/features-and-use-cases.md) document

## Setup

### Using as a package

- To use Hence as python package just run

    ```shell
    pip install -U git+https://github.com/chkware/hence.git@main
    ```

    > I intent to keep `main` branch stable. I will also release stable tags. Therefore, anyone should be able to install from a specific tag.

### Development

This software use Pipenv for development. Therefore please [install Pipenv](https://pipenv.pypa.io/en/latest/installation.html#installing-pipenv) it beforehand.

- To install the development setup

    ```shell
    pipenv install --dev
    ```

- To run a example script

    ```shell
    pipenv run python example/[SCRIPT_NAME].py
    ```

### Testing

This software use pytest for testing.

- Run all test scripts as follows

    ```shell
    pipenv run python -m pytest -s
    ```

## Contributions

- Read [CONTRIBUTING](./docs/CONTRIBUTING) document before you contribute.
- [Create issues](https://github.com/chkware/hence/issues) for any questions or request

---
Licensed under [AGPL-3.0](./LICENSE) | Follow [@chkware](https://twitter.com/chkware) on Twitter
