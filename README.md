# Banking System 🏦

This is a simple terminal-based banking application designed to help my brother learn how to contribute to a project using Git and GitHub. The project is currently a skeleton, with core features waiting to be implemented.

## Project Structure 📁

- `src/`: Contains the main application logic.
  - `main.py`: The entry point of the application.
  - `accounts.py`: (Planned) Module for managing account creation, login, etc.
  - `transactions.py`: (Planned) Module for handling deposit, withdrawal, transfers, and transaction history.
- `tests/`: Contains unit tests for the application.
  - `test_accounts.py`: Placeholder for account-related tests.
  - `data/`: Intended for storing persistent data (e.g., `accounts.json`).
- `.venv/`: Virtual environment managed by `uv`.

## Getting Started 🚀

To get this project running on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_GITHUB_REPO_URL> # Replace with the actual URL after creation
    cd banking_app_for_bro
    ```
2.  **Set up the virtual environment with `uv`:**
    ```bash
    uv venv
    ```
3.  **Activate the virtual environment:**
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .\.venv\Scripts\activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
4.  **Install dependencies (if any):**
    ```bash
    uv pip install -r requirements.txt
    ```
5.  **Run the application (current placeholder):**
    ```bash
    python src/main.py
    ```
    The application is currently very basic, prompting for features that are not yet implemented. Your task will be to implement one!

## Contribution Guide 🤝

Please refer to the open [Issues](https://github.com/testdevharshthakur/banking-system-py/issues) on GitHub for tasks to work on. When contributing:

1.  **Fork the repository** (if you don't have direct write access to this one).
2.  **Clone your forked repository** to your local machine.
3.  **Create a new branch** for your feature or bug fix. Use descriptive names like `feature/data-persistence` or `bugfix/login-issue`.
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Implement** your changes.
5.  **Write (or update) tests** for your changes in the `tests/` directory.
6.  **Commit** your changes with clear, concise commit messages. Use conventional commits if possible (e.g., `feat: Add data persistence`, `fix: Resolve login bug`).
7.  **Push** your branch to your fork on GitHub:
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request (PR)** against the `main` branch of the original repository. Provide a detailed description of your changes in the PR.
9.  Ensure your code is clean and readable.

---
*Happy Hacking!* 🚀