![badge](https://github.com/grant-baer/Picture-Perfect-Project/actions/workflows/backend-ci.yml/badge.svg)
![badge](https://github.com/grant-baer/Picture-Perfect-Project/actions/workflows/frontend-ci.yml/badge.svg)

# Picture Perfect

## About the Project

## UI Prototype

## Development Environment Setup

## Code Style Guide

To maintain code quality and ensure consistency throughout our codebase, we have adopted specific style guides for our backend and frontend code. Contributors are expected to follow these style guidelines when submitting code to the project.

### Backend (Python)

For our backend code, we follow the [pycodestyle](https://pycodestyle.pycqa.org/en/latest/) conventions, specifically version `2.11.1`. This tool checks your Python code against some of the style conventions in PEP 8.

To install pycodestyle, run the following command:

```bash
pip install pycodestyle==2.11.1
```

Before submitting a pull request, please check your code for style violations by running:

```bash
pycodestyle your_script.py
```

Replace `your_script.py` with the path to the file you want to check. Address any style warnings/errors before submitting your code.

### Frontend (Next.js)

For the frontend, we use [Next.js](https://nextjs.org/) framework and enforce code styles and conventions using ESLint and Prettier. Ensure you have the latest versions of both installed.

#### ESLint

ESLint is a static code analysis tool for identifying problematic patterns in JavaScript code.

To install ESLint, run:

```bash
npm install eslint --save-dev
```

You can then set up ESLint by following these commands:

```bash
npx eslint --init
```

Select the appropriate options that match our project's setup when prompted.

#### Prettier

Prettier is an opinionated code formatter that supports many languages and integrates with most editors.

To install Prettier, run:

```bash
npm install --save-dev --save-exact prettier
```

After installing, you can run Prettier with:

```bash
npx prettier --write .
```

This command will format your code according to the project's style guidelines.

### IDE Plugins

For a smoother coding experience, we recommend setting up your IDE with plugins for ESLint and Prettier.

#### Visual Studio Code

- **ESLint Plugin**: Install the ESLint extension by going to the Extensions view (Ctrl+Shift+X) and searching for 'ESLint' and install it.

- **Prettier Plugin**: Similarly, search for 'Prettier - Code formatter' and install the extension.

After installing the plugins, configure your settings to format on save, which can typically be done by adding the following to your settings.json file:

```json
{
  "editor.formatOnSave": true,
  "eslint.autoFixOnSave": true,
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "next",
    "next/core-web-vitals"
  ],
  "prettier.disableLanguages": []
}
```

This setup will automatically format your code according to the project's style guide when you save a file.

#### Other IDEs

For other IDEs, please refer to the respective plugin installation and configuration documentation, ensuring they match the versions and configurations we use in this project.

---

Remember to commit the style configuration files for ESLint and Prettier (`.eslintrc`, `.prettierrc`, etc.) to your project repository so that all contributors use consistent settings.

**Considerations**

- User Auth
- Interface - sign in - user portfolio - image generating (on users own portfolio) - voting - leaderboard (best creator/image)
- API cost - estimate cost for Klingenberg to cover
- Image storage - use urls for faster loading speed - openAI can host image URLs

**Programs:**
Python Flask (Backend),
React via next.js (Frontend)
MongoDB (DB)
