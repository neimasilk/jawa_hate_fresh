# Pipeline Opsi A (Pilot #6b) — PERBESAR POOL via cascade filter.
# IDEMPOTENT + resume-safe: aman dijalankan ulang kapan pun (tiap step skip yang
# sudah selesai). Kalau mesin sleep/crash di tengah, jalankan ulang script ini.
#
# Pemakaian: PowerShell di folder proyek -> .\scripts\run_cascade_pipeline.ps1
# PENTING: pastikan mesin TIDAK sleep (GPU lokal jalan berjam-jam):
#          Settings -> System -> Power -> Sleep = Never (plugged in).
#
# Catatan teknis: JANGAN pakai $ErrorActionPreference="Stop" — tqdm menulis ke
# stderr; di PS 5.1 itu jadi NativeCommandError yang membatalkan script walau
# python sukses. Pakai cek $LASTEXITCODE eksplisit + stderr di-redirect ke file.
#
# Urutan (cascade hemat $; pool tetap grok-confirmed):
#   1. SEA-LION pre-screen ~8.3K sisa (lokal, gratis)
#   2. qwen3 re-screen kandidat pass1 + grok verify kandidat pass2 (~$1.2)
#   3. regenerate pool hot-Jawa (grok-confirmed)
#   4-5. label pool baru 3-rater: deepseek+grok, lalu qwen3 lokal (resume; 332 lama di-skip)
#   6. analisis: held-out alpha + consensus dataset + profil taksonomi

$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)
$py = ".venv\Scripts\python"
$seal = "aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m"
$err = "experiments\pilot06_local_models\outputs\cascade_stderr.log"

Write-Host "[1/6] SEA-LION pass1 filter ~8.3K sisa (lokal, resume-aware)..."
$env:FILTER_VENDOR = "ollama"; $env:LOCAL_MODEL = $seal; $env:LOCAL_NO_THINK = "1"
& $py experiments\pilot02_llm_jawa_filter\run_filter.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 1 (SEA-LION pass1) gagal - jalankan ulang script (resume)." }

Write-Host "[2/6] Cascade pass2 (qwen3 re-screen) + pass3 (grok verify)..."
$env:CASCADE_PASS2_MODEL = "qwen3:14b"
& $py experiments\pilot06_local_models\run_cascade.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 2 (cascade) gagal - jalankan ulang script (resume)." }

Write-Host "[3/6] Regenerate pool hot-Jawa (grok-confirmed) -> hot_jawa_subset.jsonl..."
& $py experiments\pilot02_llm_jawa_filter\analyze.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 3 (regenerate pool) gagal." }

Write-Host "[4/6] Label pool baru 3-rater: deepseek+grok (resume; 332 lama di-skip)..."
Remove-Item Env:\LOCAL_MODEL -ErrorAction SilentlyContinue
$env:BULK_VENDORS = "deepseek,grok"
& $py experiments\pilot05_bulk_labeling\run_bulk.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 4 (label ds+grok) gagal - jalankan ulang script (resume)." }

Write-Host "[5/6] Label pool baru: qwen3 lokal (rater ke-3)..."
$env:BULK_VENDORS = "ollama"; $env:LOCAL_MODEL = "qwen3:14b"; $env:LOCAL_NO_THINK = "1"
& $py experiments\pilot05_bulk_labeling\run_bulk.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 5 (label qwen3) gagal - jalankan ulang script (resume)." }

Write-Host "[6/6] Analisis: held-out alpha + consensus dataset + profil taksonomi..."
& $py experiments\pilot05_bulk_labeling\analyze.py 2>> $err
if ($LASTEXITCODE -ne 0) { throw "Step 6 (analisis) gagal." }

Write-Host ""
Write-Host "SELESAI Opsi A. Report: experiments\pilot05_bulk_labeling\report.md"
Write-Host "Dataset: data\labeled\bulk_v2_consensus.jsonl (+ bulk_v2_disagreement.jsonl)"
