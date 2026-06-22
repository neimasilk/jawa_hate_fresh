# Resume Opsi A setelah SEA-LION pass1 selesai.
# Mulai dari cascade pass2/pass3, lalu regenerate pool, bulk label 3-rater, analisis.

$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)

$py = ".venv\Scripts\python"
$log = "experiments\pilot06_local_models\outputs\cascade_remaining_pipeline.log"

Start-Transcript -Path $log -Append | Out-Null
try {
    $env:CASCADE_PASS2_MODEL = "qwen3:14b"

    Write-Host "[2/6] Cascade pass2 resume + pass3 grok verify..."
    & $py experiments\pilot06_local_models\run_cascade.py
    if ($LASTEXITCODE -ne 0) { throw "Step 2 cascade failed." }

    Write-Host "[3/6] Regenerate pool hot-Jawa (grok-confirmed)..."
    & $py experiments\pilot02_llm_jawa_filter\analyze.py
    if ($LASTEXITCODE -ne 0) { throw "Step 3 filter analyze failed." }

    Write-Host "[4/6] Label pool baru: deepseek+grok..."
    Remove-Item Env:\LOCAL_MODEL -ErrorAction SilentlyContinue
    $env:BULK_VENDORS = "deepseek,grok"
    & $py experiments\pilot05_bulk_labeling\run_bulk.py
    if ($LASTEXITCODE -ne 0) { throw "Step 4 bulk cloud failed." }

    Write-Host "[5/6] Label pool baru: qwen3 lokal..."
    $env:BULK_VENDORS = "ollama"
    $env:LOCAL_MODEL = "qwen3:14b"
    $env:LOCAL_NO_THINK = "1"
    & $py experiments\pilot05_bulk_labeling\run_bulk.py
    if ($LASTEXITCODE -ne 0) { throw "Step 5 bulk qwen3 failed." }

    Write-Host "[6/6] Analisis final..."
    & $py experiments\pilot05_bulk_labeling\analyze.py
    if ($LASTEXITCODE -ne 0) { throw "Step 6 final analyze failed." }

    Write-Host "DONE remaining pipeline."
}
finally {
    Stop-Transcript | Out-Null
}
