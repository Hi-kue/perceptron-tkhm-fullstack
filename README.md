<div align="left">
<a href="/url">
    <img src="./assets/alfai-logo.svg" alt="Alfred AI Logo" height="150">
</a>

<h3 align="left">
    Alfred AI Take Home Assessment
</h3>

<p align="left">
    Take home assessment for Perceptron Labs, intended for submission including a 
    <a href="/url">link to the deployed project</a> and a following all requirements
    <a href="/url">here</a>.
    <br />
</p>


<div align="center">
    <a href="/url">Report Bug</a>
    ✱
    <a href="/url">Request Feature</a>
    ✱
    <a href="/url">Documentation</a>
</div>
</div>

## Project Description

> [!WARNING]
> This project is intended to be a submission for Perceptron Labs, and is not intended to be used for commercial purposes.

This project is a take home assement for Perceptron Labs, and is intended to be a submission for the
following the requirements for building a LLM Chatbot with the personality of Alfred. The project is
deployed on Fly.io, and can be accessed at the following link: [Alfred AI](https://alfred-ai.fly.dev).

Alfred AI is an intelligent chatbot that embodies the persona of Alfred Pennyworth, the loyal butler from Batman. Using LangChain and OpenAI's language model, Alfred AI provides clothing recommendations based on the user's specified location and weather conditions. The chatbot maintains Alfred's characteristic wit, formality, and attention to detail in its responses.

## Features

- Natural language interaction mimicking Alfred's persona
- Real-time weather data integration
- Personalized clothing recommendations based on location and weather
- Deployment on Fly.io for easy access

## Getting Started

### Prerequisites

To run this project locally, you'll need:

- `Python 3.12+`
- `OpenAI` API key
- `LangChain` API key

### Installation

To get started with the project simply start first with cloning the repository:

```bash
git clone https://github.com/Hi-kue/perceptron-tkhm-fullstack.git
cd alfred-ai
```

Set your virtual environment (or just use poetry):
```bash
# using venv
python -m venv venv
use venv\Scripts\activate

# using poetry
poetry install
poetry shell
poetry update || lock
```

If you did not use poetry, then install the packages:
```bash
pip install -r requirements.txt
```

Next, create a `.env` file in the project root and add your API keys:
```bash
OPENAI_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=...
```

> NOTE: Follow the `.env.example` file for the required .env file, 
> I will be providing it in the submission for this.


And you should be good to go! All you need to do now is run the chatbot:
```bash
py main.py
```

## Technology Stack
- Python
- LangChain
- OpenAI GPT
- DuckDuckGo Search API (For the `Weather Data`)
- Fly.io (For Deployment)

## Future Considerations
- [Tavily](https://docs.tavily.com/) (Engine Optimizations for LLMs)

## License

Distributed under the MIT License. See `LICENSE` for more information.

![License](https://img.shields.io/github/license/Hi-kue/perceptron-tkhm-fullstack?style=default-rect)