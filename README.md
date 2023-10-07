# LLMRails Python SDK

This package provides functionality developed to simplify interfacing with the [LLMRails API](https://docs.llmrails.com/) in Python 3.

## Documentation

* For more details on advanced parameters, you can also consult the [API documentation](https://docs.llmrails.com/).

## Installation

The package can be installed with `pip`:

```bash
pip install --upgrade llmrails
```

Install from source:

```bash
pip install .
```

### Requirements

- Python 3.7+

## Quick Start

To use this library, you must have an API key and specify it as a string when creating the `llmrails.Client` object. API keys can be created through the [platform](https://console.llmrails.com/api-keys). This is a basic example of the creating the client and using the `generate` endpoint.

```python
import llmrails

# initialize the LLMRails Client with an API Key
rails = llmrails.Client('YOUR_API_KEY')

# generate a prediction for a prompt
embeddings = rails.embed(
            model='embedding-english-v1',
            text=['Hey There'])

# print the predicted text
print('embeddings: {}'.format(embeddings.data[0].embedding))
```