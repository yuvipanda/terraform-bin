[![build status](https://github.com/yuvipanda/terraform-bin/actions/workflows/main.yml/badge.svg)](https://github.com/shellcheck-py/shellcheck-py/actions/workflows/main.yml)

# terraform-bin

(Copied almost verbatim from [shellcheck-py](https://github.com/shellcheck-py/shellcheck-py/))

A python wrapper to provide a pip-installable [terraform] binary.

Internally this package provides a convenient way to download the pre-built
shellcheck binary for your particular platform.

### installation

```bash
pip install terraform-bin
```

### usage

After installation, the `terraform` binary should be available in your
environment (or `terraform.exe` on windows).

### As a pre-commit hook

See [pre-commit] for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/-py/shellcheck-py
    rev: v0.9.0.2
    hooks:
    -   id: shellcheck
```

[terraform]: https://www.terraform.io/
[pre-commit]: https://pre-commit.com
