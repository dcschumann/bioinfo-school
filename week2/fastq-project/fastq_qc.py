#!/usr/bin/env python3
"""
FASTQ Quality Control (QC) Analyzer
Reads a FASTQ file (compressed or plaintext), calculates key QC metrics,
and generates a premium, responsive single-page HTML report with interactive plots.
"""

import os
import sys
import gzip
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(
        description="FASTQ Quality Control (QC) Analyzer and Reporter"
    )
    parser.add_argument(
        "fastq", 
        help="Path to the input FASTQ file (can be plaintext .fastq/.fq or gzipped .fastq.gz/.fq.gz)"
    )
    parser.add_argument(
        "-o", "--output",
        default="qc_report.html",
        help="Path to save the generated HTML report (default: qc_report.html)"
    )
    parser.add_argument(
        "--phred",
        choices=["33", "64", "auto"],
        default="auto",
        help="Phred quality score offset. 'auto' will attempt to auto-detect the encoding (default: auto)"
    )
    return parser.parse_args()

def open_fastq(file_path):
    """
    Safely opens a FASTQ file supporting both plaintext and gzip formats.
    """
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    else:
        return open(file_path, 'r', encoding='utf-8', errors='ignore')

def detect_phred_encoding(file_path, num_records=1000):
    """
    Heuristically autodetects Phred offset (33 or 64) by examining the ASCII range
    of quality strings in the first N records.
    """
    min_ascii = 127
    max_ascii = 0
    records_checked = 0
    
    try:
        with open_fastq(file_path) as f:
            state = 0
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if state % 4 == 3:
                    for char in line:
                        ascii_val = ord(char)
                        if ascii_val < min_ascii:
                            min_ascii = ascii_val
                        if ascii_val > max_ascii:
                            max_ascii = ascii_val
                    records_checked += 1
                    if records_checked >= num_records:
                        break
                state += 1
    except Exception:
        pass
        
    # If we observed any quality characters below ASCII 64, it must be Phred+33.
    # Otherwise, if we saw high-range values (> 74) and no low-range values, it is highly likely Phred+64.
    if min_ascii < 64:
        return 33
    elif max_ascii > 74:
        return 64
    else:
        # Default to 33 if ambiguous (modern sequencing data)
        return 33

def run_qc(file_path, phred_option="auto"):
    """
    Parses the FASTQ file line-by-line and calculates core QC metrics.
    """
    num_reads = 0
    total_bases = 0
    gc_bases = 0
    q30_bases = 0
    
    # Determine Phred offset
    if phred_option == "auto":
        phred_offset = detect_phred_encoding(file_path)
        print(f"Auto-detected quality encoding offset: Phred+{phred_offset}")
    else:
        phred_offset = int(phred_option)
        print(f"Using user-specified quality encoding offset: Phred+{phred_offset}")
        
    # Store quality sums and counts per position (for variable length reads)
    qual_sums = []
    qual_counts = []
    
    print(f"Analyzing FASTQ file: {file_path}...")
    
    try:
        with open_fastq(file_path) as f:
            state = 0  # 0: header, 1: sequence, 2: separator (+), 3: quality
            current_seq = ""
            
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                mod_state = state % 4
                
                if mod_state == 0:
                    # Header line
                    if not line.startswith('@'):
                        raise ValueError(f"Line {line_num} does not start with '@' as expected for a FASTQ header.")
                    num_reads += 1
                elif mod_state == 1:
                    # Sequence line
                    current_seq = line
                    seq_len = len(current_seq)
                    total_bases += seq_len
                    gc_bases += sum(1 for base in current_seq if base in 'GCgc')
                elif mod_state == 2:
                    # Plus line
                    if not line.startswith('+'):
                        raise ValueError(f"Line {line_num} does not start with '+' as expected for a FASTQ separator.")
                elif mod_state == 3:
                    # Quality line
                    qual_str = line
                    if len(qual_str) != len(current_seq):
                        raise ValueError(f"Line {line_num}: Quality string length ({len(qual_str)}) does not match sequence length ({len(current_seq)}).")
                    
                    # Compute Phred scores
                    for i, char in enumerate(qual_str):
                        q_score = ord(char) - phred_offset
                        if q_score >= 30:
                            q30_bases += 1
                            
                        # Extend the position tracking arrays if needed
                        if i >= len(qual_sums):
                            qual_sums.append(0)
                            qual_counts.append(0)
                        
                        qual_sums[i] += q_score
                        qual_counts[i] += 1
                
                state += 1
                
    except Exception as e:
        print(f"Error reading FASTQ file at line {line_num if 'line_num' in locals() else 'unknown'}: {e}", file=sys.stderr)
        sys.exit(1)
        
    if num_reads == 0:
        print("Error: No reads found in the specified file.", file=sys.stderr)
        sys.exit(1)
        
    # Calculate stats
    avg_read_length = total_bases / num_reads
    gc_content_pct = (gc_bases / total_bases) * 100 if total_bases > 0 else 0
    q30_pct = (q30_bases / total_bases) * 100 if total_bases > 0 else 0
    
    # Calculate mean quality per position
    mean_quals = []
    positions = []
    for i in range(len(qual_sums)):
        positions.append(i + 1)
        mean_quals.append(round(qual_sums[i] / qual_counts[i], 2) if qual_counts[i] > 0 else 0)
        
    return {
        "filename": os.path.basename(file_path),
        "num_reads": num_reads,
        "total_bases": total_bases,
        "avg_read_length": round(avg_read_length, 2),
        "gc_content_pct": round(gc_content_pct, 2),
        "q30_pct": round(q30_pct, 2),
        "positions": positions,
        "mean_quals": mean_quals,
        "phred_offset": phred_offset
    }

def generate_report(stats, output_path):
    """
    Generates a premium, responsive dark-themed HTML report incorporating Chart.js.
    """
    # Determine basic status indicators based on general thresholds
    q30_status = "Excellent" if stats["q30_pct"] >= 80 else ("Acceptable" if stats["q30_pct"] >= 70 else "Poor")
    q30_color = "status-green" if q30_status == "Excellent" else ("status-yellow" if q30_status == "Acceptable" else "status-red")
    
    gc_status = "Normal" if 30 <= stats["gc_content_pct"] <= 60 else "Unusual"
    gc_color = "status-green" if gc_status == "Normal" else "status-yellow"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FASTQ QC Report - {stats["filename"]}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: #151d30;
            --border-color: #222f4c;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-primary: #3b82f6;
            --accent-secondary: #10b981;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --font-outfit: 'Outfit', sans-serif;
            --font-inter: 'Inter', sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: var(--font-inter);
            padding: 2rem 1.5rem;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        h1 {{
            font-family: var(--font-outfit);
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
        }}

        .file-info {{
            font-size: 0.95rem;
            color: var(--text-secondary);
        }}

        .timestamp {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            background: var(--card-bg);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .card:hover {{
            transform: translateY(-2px);
            border-color: #3b82f640;
        }}

        .card-title {{
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        .card-value {{
            font-family: var(--font-outfit);
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .card-subtitle {{
            font-size: 0.8rem;
            margin-top: 0.25rem;
        }}

        .status-green {{
            color: var(--success);
        }}

        .status-yellow {{
            color: var(--warning);
        }}

        .status-red {{
            color: var(--danger);
        }}

        .main-layout {{
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 1.5rem;
        }}

        @media (max-width: 900px) {{
            .main-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-container {{
            min-height: 400px;
        }}

        .table-container {{
            display: flex;
            flex-direction: column;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            font-size: 0.9rem;
        }}

        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            font-weight: 600;
            color: var(--text-secondary);
            background-color: rgba(255, 255, 255, 0.02);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .badge {{
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-success {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--success);
        }}

        .badge-warning {{
            background-color: rgba(245, 158, 11, 0.15);
            color: var(--warning);
        }}

        footer {{
            margin-top: 4rem;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            padding-top: 1.5rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>FASTQ Quality Control</h1>
                <div class="file-info">File Analyzed: <strong>{stats["filename"]}</strong></div>
            </div>
            <div class="timestamp">
                Generated: <span id="time-span"></span>
            </div>
        </header>

        <section class="stats-grid">
            <div class="card">
                <div class="card-title">Total Reads</div>
                <div class="card-value">{stats["num_reads"]:,}</div>
                <div class="card-subtitle status-green">Sequence records parsed</div>
            </div>
            <div class="card">
                <div class="card-title">GC Content</div>
                <div class="card-value">{stats["gc_content_pct"]}%</div>
                <div class="card-subtitle {gc_color}">{gc_status} distribution</div>
            </div>
            <div class="card">
                <div class="card-title">Avg Read Length</div>
                <div class="card-value">{stats["avg_read_length"]} bp</div>
                <div class="card-subtitle status-green">Average base pairs per read</div>
            </div>
            <div class="card">
                <div class="card-title">Bases &ge; Q30</div>
                <div class="card-value">{stats["q30_pct"]}%</div>
                <div class="card-subtitle {q30_color}">Phred score &ge; 30 ({q30_status})</div>
            </div>
        </section>

        <main class="main-layout">
            <div class="card chart-container">
                <div class="card-title">Mean Phred Quality Score per Position</div>
                <div style="position: relative; height: 350px; width: 100%;">
                    <canvas id="qualityChart"></canvas>
                </div>
            </div>

            <div class="card table-container">
                <div class="card-title">QC Metrics Summary Table</div>
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total Reads</td>
                            <td>{stats["num_reads"]:,}</td>
                            <td><span class="badge badge-success">Pass</span></td>
                        </tr>
                        <tr>
                            <td>Total Bases</td>
                            <td>{stats["total_bases"]:,} bp</td>
                            <td><span class="badge badge-success">Pass</span></td>
                        </tr>
                        <tr>
                            <td>Avg Read Length</td>
                            <td>{stats["avg_read_length"]} bp</td>
                            <td><span class="badge badge-success">Pass</span></td>
                        </tr>
                        <tr>
                            <td>GC Content</td>
                            <td>{stats["gc_content_pct"]}%</td>
                            <td><span class="badge {"badge-success" if gc_status == "Normal" else "badge-warning"}">{gc_status}</span></td>
                        </tr>
                        <tr>
                            <td>Q30 Bases</td>
                            <td>{stats["q30_pct"]}%</td>
                            <td><span class="badge {"badge-success" if q30_status == "Excellent" or q30_status == "Acceptable" else "badge-warning"}">{q30_status}</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>

        <footer>
            FASTQ QC Analyzer &bull; Generated dynamically in pure Python and Chart.js
        </footer>
    </div>

    <script>
        // Set dynamic local timestamp
        document.getElementById('time-span').textContent = new Date().toLocaleString();

        // Chart.js Configuration
        const ctx = document.getElementById('qualityChart').getContext('2d');
        const positions = {json.dumps(stats["positions"])};
        const meanQuals = {json.dumps(stats["mean_quals"])};

        // Create elegant color gradient for the line
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: positions,
                datasets: [{{
                    label: 'Mean Quality Score',
                    data: meanQuals,
                    borderColor: '#3b82f6',
                    borderWidth: 3,
                    pointBackgroundColor: '#60a5fa',
                    pointBorderColor: '#151d30',
                    pointHoverBackgroundColor: '#10b981',
                    pointHoverBorderColor: '#ffffff',
                    pointRadius: positions.length > 50 ? 0 : 4,
                    pointHoverRadius: 6,
                    fill: true,
                    backgroundColor: gradient,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        backgroundColor: '#1e293b',
                        titleColor: '#f3f4f6',
                        bodyColor: '#9ca3af',
                        borderColor: '#334155',
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {{
                            title: function(context) {{
                                return 'Position: ' + context[0].label + ' bp';
                            }},
                            label: function(context) {{
                                return 'Mean Phred Score: ' + context.parsed.y;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        min: 0,
                        max: 45,
                        grid: {{
                            color: '#222f4c',
                            drawBorder: false
                        }},
                        ticks: {{
                            color: '#9ca3af',
                            font: {{
                                family: 'Inter'
                            }}
                        }},
                        title: {{
                            display: true,
                            text: 'Phred Quality Score (Q)',
                            color: '#9ca3af',
                            font: {{
                                family: 'Inter',
                                size: 12,
                                weight: 500
                            }}
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }},
                        ticks: {{
                            color: '#9ca3af',
                            font: {{
                                family: 'Inter'
                            }}
                        }},
                        title: {{
                            display: true,
                            text: 'Position in Read (bp)',
                            color: '#9ca3af',
                            font: {{
                                family: 'Inter',
                                size: 12,
                                weight: 500
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Report generated successfully: {output_path}")

def main():
    args = parse_args()
    if not os.path.exists(args.fastq):
        print(f"Error: File not found: {args.fastq}", file=sys.stderr)
        sys.exit(1)
        
    stats = run_qc(args.fastq, args.phred)
    generate_report(stats, args.output)

if __name__ == "__main__":
    main()
