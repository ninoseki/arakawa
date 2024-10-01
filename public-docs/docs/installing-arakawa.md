---
description: Installing and setting up the Arakawa library and API on your device
---

Datapane's Python library and CLI can be installed using either `pip` or `conda` on macOS, Windows, or Linux. Datapane supports Python **3.9 - 3.12**.

!!! info

    Instructions for installing Python can be found at [https://wiki.python.org/moin/BeginnersGuide/Download](https://wiki.python.org/moin/BeginnersGuide/Download).

## pip

If you use `pip`, you can install it with:

=== "Shell"

    ```bash
    pip3 install -U arakawa
    ```

=== "Jupyter"

    ```bash
    !pip3 install -U arakawa
    ```

## conda

If you use `conda`, you can install it with:

=== "Shell"

    ```bash
    conda install -c conda-forge arakawa
    ```

=== "Jupyter"

    ```bash
    !conda install -c conda-forge arakawa
    ```

!!! warning
Conda sometimes installs an older version of Datapane. If you receive errors, please check the version and try running `conda update --all` or try in a new conda environment (`conda create -n ENV` and `conda activate ENV`)

## Upgrading

### Upgrading via pip

If you installed Arakawa via pip, run the following command:

```bash
pip install -U arakawa
```

### Upgrading via conda

If you installed `arakawa` via conda, run the following command, adding the `--all` flag if needed. As above, if you receive errors please try using a fresh conda environment.

```bash
conda update arakawa OR conda update --all
```
