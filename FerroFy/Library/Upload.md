# 📦 Build and Upload Python Package

## 📁 Steps

1. 🛠️ **Build dist/***

```bash
python -m build
```

2. 🚀 **Upload the package to PyPI using Twine**

```bash
twine upload dist/*
```

3. **Add Your API Key**

# ⚠️ Note

- 🔢 Always upgrade the version number in setup.py before building, otherwise upload may fail.