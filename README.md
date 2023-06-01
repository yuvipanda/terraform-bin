[![build status](https://github.com/yuvipanda/terraform-bin/actions/workflows/main.yml/badge.svg)](https://github.com/shellcheck-py/shellcheck-py/actions/workflows/main.yml)

# terraform-bin

(Copied almost verbatim from [shellcheck-py](https://github.com/shellcheck-py/shellcheck-py/))

A python wrapper to provide a pip-installable [terraform] binary,
primarily for use with [pre-commit.ci](https://pre-commit.ci). It does
not allow us to install `terraform` easily there, so we wrap it into PyPI.

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

- repo: https://github.com/yuvipanda/terraform-bin
  rev: v1.0.0
  hooks:
    - id: terraform-fmt
```

[terraform]: https://www.terraform.io/
[pre-commit]: https://pre-commit.com
