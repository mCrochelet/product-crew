# Problem to solve

As a developer, I can choose the model provider I want to work with (either 
Anthropic or OpenAI).

# Acceptance criteria

only valid models from OPENAI or Anthropic are accepted
the CLI should exit with error code 1 if the model is not valid
by default, the CLI should use the model gpt-4o from OPENAI
The argument is optional