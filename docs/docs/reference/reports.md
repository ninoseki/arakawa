# Reports

Once you have built up the blocks that make up your report, you can use the following methods to save it as a local report.

```py
import arakawa as ar

report = ar.Report(ar.Text("Hello, world!"))
report.save("report.html")
# or
report.stringify()
```

::: arakawa.view.view_blocks.Report

Alternatively, you can use the following functions to save or stringify a report or blocks.

::: arakawa.processors.api.save_report

::: arakawa.processors.api.stringify_report

## Standalone Mode

A report uses CDN (jsDelivr) to load assets by default.

As an alternative, you can use standalone mode which inlines assets in a report.

```py
report.save("report.html", standalone=True)
# or
report.stringify(standalone=True)
```

!!! note

    Inlining assets significantly increases the size of a report. The size can exceed 20MB.

## In-House CDN

There is an option to use an in-house CDN by configuring CDN URL via `AR_CDN_BASE` environment variable (defaults to `https://cdn.jsdelivr.net/npm/arakawa@{VERSION)/dist`).

- Download frontend assets via jsDelivr or NPM:
  - https://www.jsdelivr.com/package/npm/arakawa
  - https://www.npmjs.com/package/arakawa (`npm pack arakawa` to download)
- Unpack it and upload files into your CDN (e.g. S3 or S3-like object storage)

```bash
AR_CDN_BASE=http://... python report.py
```
