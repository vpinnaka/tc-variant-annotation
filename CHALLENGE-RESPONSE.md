## Instruction to install the annotate-variants locally
______________________________________________________



### Install dependencies

```
pip install -r requirements.txt
```

### Build and Package the annotate-variants tool
```
python3 -m build
```

### Install the annotate-variants tool
```
pip install dist/annotate_variants-0.0.1-py3-none-any.whl --force-reinstall
```

### Run the annotate-variants tool
```
annotate-variants variants.txt annotations.tsv
```
