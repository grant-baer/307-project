![badge](https://github.com/grant-baer/Picture-Perfect-Project/actions/workflows/backend-ci.yml/badge.svg)
![badge](https://github.com/grant-baer/Picture-Perfect-Project/actions/workflows/frontend-ci.yml/badge.svg)

# Picture Perfect

## About the Project

### Description

Picture Perfect is an AI-powered game designed to challenge your creativity! Input any text-based prompt you can imagine and get back a realistic image. The better the prompt, the better the image! Once you have prompt engineered to your heart's content, check out the voting page where images compete for your vote, king of the hill style. Check out the leaderboard to see how you fare in comparison to other PicPerfers!

### Tech Stack

### Backend

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

### Frontend

- ![Next JS](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white)
- ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
- ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python]: https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white
[HTML-URL]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[CSS-URL]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white

## Installation and Setup

1. Make sure you have [Python](https://www.python.org/downloads/) and [Node](https://nodejs.org/en/download) environments set up (this includes npm and pip3). The latest stable releases should be fine as of December 2023, but this project uses Node v20 and Python 3.10.

2. Installing the frontend packages:
   From root:
   - `cd Frontend`
   - `npm install`
3. Installing the backend packages:
   From root:

   - `cd Backend`
   - `pip3 install -r requirements.txt`

4. Currently, the frontend is hosted locally. Run it with the command `npm run dev` in the Frontend folder.

## UI Prototype

## Code Coverage

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
