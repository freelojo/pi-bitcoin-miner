# Contributing to Raspberry Pi Bitcoin Miner

Thank you for your interest in contributing to this educational project!

## Getting Started

### Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/pi-bitcoin-miner.git
   cd pi-bitcoin-miner
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks** (optional but recommended)

   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Code Style

We follow Python best practices and PEP 8 style guidelines.

### Formatting

- Use **Black** for code formatting:
  ```bash
  black controller/ tests/
  ```

- Use **isort** for import sorting:
  ```bash
  isort controller/ tests/
  ```

### Linting

- Run **flake8** for style checking:
  ```bash
  flake8 controller/ tests/
  ```

- Run **pylint** for code analysis:
  ```bash
  pylint controller/
  ```

### Type Checking

- Run **mypy** for type checking:
  ```bash
  mypy controller/
  ```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=controller

# Run specific test file
pytest tests/test_worker_manager.py

# Run specific test
pytest tests/test_worker_manager.py::test_pico_worker_init
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use pytest fixtures for setup/teardown
- Mock hardware interactions (serial, network)
- Aim for >80% code coverage

Example test:

```python
import pytest
from controller.worker_manager import PicoWorker

def test_worker_initialization():
    """Test that worker initializes correctly"""
    worker = PicoWorker('/dev/ttyACM0', 0)
    assert worker.worker_id == 0
    assert worker.is_connected is False
```

## Project Structure

```text
pi-bitcoin-miner/
├── controller/          # Main controller code
│   ├── main.py         # Entry point
│   ├── worker_manager.py
│   ├── mining_coordinator.py
│   ├── pool_client.py
│   └── dashboard.py
├── pico_firmware/      # Pico MicroPython code
│   ├── boot.py
│   └── main.py
├── config/             # Configuration files
├── tests/              # Test suite
├── docs/               # Documentation
└── scripts/            # Setup and utility scripts
```

## Making Changes

### Workflow

1. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**

   ```bash
   pytest
   mypy controller/
   black controller/ tests/
   ```

4. **Commit your changes**

   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Convention

Use conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

Examples:

```text
feat: add hashrate optimization for Pico workers
fix: resolve serial communication timeout issue
docs: update setup instructions for Windows
test: add unit tests for mining coordinator
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Submit PR** with clear description

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Type hints added for new functions
- [ ] No lint/type errors
- [ ] Commit messages follow convention

## Areas for Contribution

### High Priority

- SHA-256 optimization for Pico
- Improved error handling and recovery
- Better work distribution algorithms
- Performance monitoring and metrics

### Medium Priority

- Web-based dashboard
- Support for more mining pools
- Automatic worker health checks
- Configuration validation

### Documentation

- Setup guides for different platforms
- Troubleshooting guides
- Architecture documentation
- Video tutorials

### Test Coverage Improvements

- Integration tests
- Hardware simulation tests
- Performance benchmarks
- Stress testing

## Hardware Testing

If contributing hardware-related changes:

1. Test with actual Raspberry Pi Pico devices
2. Document hardware setup used
3. Include performance measurements
4. Note any hardware-specific quirks

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Check existing issues/discussions first

## Code of Conduct

- Be respectful and constructive
- Help newcomers learn
- Focus on the technical merit of ideas
- Remember this is an educational project

## License

By contributing, you agree that your contributions will be licensed
under the MIT License.

## Thank You

Your contributions help make this educational project better for
everyone learning about Bitcoin mining, embedded systems, and
distributed computing!
