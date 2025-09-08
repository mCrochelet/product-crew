# Problem to solve

When validating the CLI arguments, also check that the open ai key is available
in the env, otherwise exit with an error; then remove all other conditional
behaviour based on the fact that the key exists (e.g., line 47 of runner) 