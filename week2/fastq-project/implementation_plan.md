# FASTQ QC Analyzer and HTML Reporter

This plan details a zero-dependency Python script that reads a FASTQ file (supporting both plaintext `.fastq` and gzipped `.fastq.gz` formats), computes core Quality Control (QC) metrics, and generates a stunning, premium, one-page interactive HTML report.

## Design Decisions

To make the script incredibly portable and easy to run on any machine without complex installation steps, we will:
1. **Use Pure Python**: Avoid dependencies like `biopython`, `pandas`, `numpy`, or `matplotlib`. Python's standard library (`gzip`, `collections`, etc.) is fully sufficient.
2. **Build an Interactive HTML Report**: Instead of generating a static image plot (e.g., using `matplotlib` which requires installation), the Python script will inject data into an HTML template containing a modern interactive charting library (e.g., **Chart.js** or **Plotly.js** via CDN). This allows the user to hover over data points, zoom, and interact with the quality-per-position plot directly in their browser.
3. **Premium Visual Styling**: The HTML report will feature a modern dark/light card-based interface, smooth transitions, high-contrast typography (Inter/Outfit), and clear visual status indicators (e.g., green/yellow/red color coding based on standard quality thresholds).

---

## Proposed Changes

### [New Script Component]

#### [NEW] [fastq_qc.py](file:///c:/Users/gesti/OneDrive/Dokumente/GitHub/fastq_qc.py)
A standalone Python 3 script.

**Core features of the script:**
- Accepts input FASTQ file path and output HTML report path via command line arguments.
- Safely handles `.fastq` and `.fastq.gz` formats automatically using `gzip`.
- Streams the FASTQ file line-by-line to handle large files efficiently with minimal memory usage.
- Computes:
  - Total number of reads
  - Total number of bases
  - Average read length
  - GC Content (%)
  - Position-wise mean Phred quality score (PHRED33 encoding: `ord(char) - 33`)
  - Basic quality status (e.g., % of bases Q30+).
- Injects computed metrics into a beautiful HTML template.

---

## Verification Plan

### Automated/Manual Verification
- Create a small dummy FASTQ file with known sequences and quality scores.
- Run `python fastq_qc.py dummy.fastq report.html`.
- Open `report.html` in a web browser and verify:
  - Accurate counts and statistics.
  - Interactive, responsive, and visually stunning charts and tables.
  - Responsive layout (mobile/desktop).
