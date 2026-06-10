# Pipeline bulk Pilot #5 — IDEMPOTENT: aman dijalankan ulang kapan pun
# (semua step resume-aware; step selesai = skip otomatis, lanjut dari sisa).
#
# Pemakaian: buka PowerShell di folder proyek, jalankan:
#   .\scripts\run_bulk_pipeline.ps1
#
# Urutan: filter full haipradana (Grok) -> regenerate pool hot-Jawa ->
#         bulk label v2 (deepseek+grok) -> analisis (held-out alpha + dataset)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "[1/4] Filter full haipradana (~12.7K, resume-aware)..."
.venv\Scripts\python experiments\pilot02_llm_jawa_filter\run_filter.py
if ($LASTEXITCODE -ne 0) { throw "Step 1 (filter) gagal - cek error di atas, lalu jalankan ulang script ini." }

Write-Host "[2/4] Regenerate pool hot-Jawa..."
.venv\Scripts\python experiments\pilot02_llm_jawa_filter\analyze.py
if ($LASTEXITCODE -ne 0) { throw "Step 2 (pool) gagal." }

Write-Host "[3/4] Bulk label prompt v2 x deepseek+grok (resume-aware)..."
.venv\Scripts\python experiments\pilot05_bulk_labeling\run_bulk.py
if ($LASTEXITCODE -ne 0) { throw "Step 3 (label) gagal - cek error, lalu jalankan ulang script ini." }

Write-Host "[4/4] Analisis: held-out alpha + consensus dataset..."
.venv\Scripts\python experiments\pilot05_bulk_labeling\analyze.py
if ($LASTEXITCODE -ne 0) { throw "Step 4 (analisis) gagal." }

Write-Host ""
Write-Host "SELESAI. Baca: experiments\pilot05_bulk_labeling\report.md"
Write-Host "Dataset:  data\labeled\bulk_v2_consensus.jsonl (+ bulk_v2_disagreement.jsonl)"
