---
title: "Tutorial: Extracting PDFs"
description: Step-by-step tutorial for extracting text from PDFs including OCR, tables, and password-protected files
section: tutorials
order: 3
---

# Tutorial: Extracting PDFs

Learn how to extract technical documentation from PDFs and create searchable AI skills.

**Time:** 10 minutes | **Level:** Beginner | **Result:** PDF-based skill

---

## Basic PDF Extraction

```bash
nexus-core pdf \
  --input /path/to/manual.pdf \
  --output output/manual/
```

## OCR for Scanned PDFs

```bash
# Install Tesseract first
# Ubuntu: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract

nexus-core pdf \
  --input /path/to/scanned.pdf \
  --output output/scanned/ \
  --ocr
```

## Password-Protected PDFs

```bash
nexus-core pdf \
  --input /path/to/encrypted.pdf \
  --output output/encrypted/ \
  --password "your-password"
```

## Extract Tables

```bash
nexus-core pdf \
  --input /path/to/spec.pdf \
  --output output/spec/ \
  --extract-tables
```

## Parallel Processing (3x Faster)

```bash
nexus-core pdf \
  --input /path/to/large.pdf \
  --output output/large/ \
  --parallel \
  --workers 8
```

**See:** [PDF Scraping Manual](/docs/manual/scraping/pdf) for complete guide.
