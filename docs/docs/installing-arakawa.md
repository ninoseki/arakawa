---
description: Installing and setting up the Arakawa library and API on your device
---

Arakawa's Python library and CLI can be installed using either `pip` or `conda` on macOS, Windows, or Linux. Arakawa supports Python **3.9 - 3.12**.

!!! info

    Instructions for installing Python can be found at [https://wiki.python.org/moin/BeginnersGuide/Download](https://wiki.python.org/moin/BeginnersGuide/Download).

## Pip

If you use `pip`, you can install it with:

=== "Shell"

    ```bash
    pip install -U arakawa
    ```

=== "Jupyter"

    ```bash
    !pip install -U arakawa
    ```

## Conda

!!! warning

    The Conda package is not yet released. The following explanation will be available soon. Please use `pip` instead for a while.

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

    Conda sometimes installs an older version of Arakawa. If you receive errors, please check the version and try running `conda update --all` or try in a new conda environment (`conda create -n ENV` and `conda activate ENV`)

## With Extras

`arakawa` comes with Pandas (for data-framing) and Altair (for plotting) by default.

You can install extra dependencies by using `plotting`, `tabling`, `network` and `datafraiming` extras.

```bash
pip install arakawa[dataframing]
pip install arakawa[network]
pip install arakawa[plotting]
pip install arakawa[tabling]
# install all the extra dependencies
pip install arakawa[all]
```

| Name          | Dependencies                         |
| ------------- | ------------------------------------ |
| `dataframing` | Polars                               |
| `network`     | NetworkX                             |
| `plotting`    | Bokeh, Folium, Matplotlib and Plotly |
| `tabling`     | Great Tables                         |

## Upgrading

### Upgrading Via Pip

If you installed Arakawa via pip, run the following command:

```bash
pip install -U arakawa
```

### Upgrading Via Conda

!!! warning

    The Conda package is not yet released. The following explanation will be available soon. Please use `pip` instead for a while.

If you installed `arakawa` via conda, run the following command, adding the `--all` flag if needed. As above, if you receive errors please try using a fresh conda environment.

```bash
conda update arakawa
# or
conda update --all
```
