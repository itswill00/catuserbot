# Contributing to CatUserBot

First off, thank you for considering contributing to CatUserBot! It's people like you who make this project better for everyone.

## Code of Conduct

By participating in this project, you agree to abide by our standards of respect and professionalism.

## How Can I Contribute?

### Reporting Bugs
* Check the existing issues to see if the bug has already been reported.
* If not, create a new issue. Include a clear title, description, and steps to reproduce.
* Attach logs or screenshots if possible.

### Suggesting Enhancements
* Open an issue with the "enhancement" tag.
* Explain why this feature would be useful and how it should work.

### Pull Requests
1. **Fork the repo** and create your branch from `master`.
2. **Setup your environment** using `./setup.sh`.
3. **Make your changes**. Ensure your code follows the existing style (PEP 8 for Python).
4. **Test your changes**. Run the bot locally and verify the feature works as expected.
5. **Commit with Sign-off**. Use `git commit -s` to sign off your commits.
6. **Submit a Pull Request** with a detailed description of what you did.

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/catuserbot.git
   cd catuserbot
   ```
2. Run setup:
   ```bash
   ./setup.sh
   ```
3. Activate environment:
   ```bash
   source venv/bin/activate
   ```
4. Run the bot:
   ```bash
   python3 -m userbot
   ```

## Coding Guidelines
* Use descriptive variable and function names.
* Keep functions small and focused on a single task.
* Use `async/await` properly for Telethon operations.
* Avoid using generic `except Exception:`; catch specific errors instead.
* Document new helper functions in `userbot/helpers/`.

## Signing Your Work
We require all commits to be signed off. This is a simple way to certify that you have the right to submit the code. You can do this by adding `-s` to your commit command:
```bash
git commit -s -m "Brief description of changes"
```

Thank you for your help!
