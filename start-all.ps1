$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
$frontend = Join-Path $root "frontend"

if (-not (Test-Path $python)) {
    throw "Python virtual environment not found: $python"
}

if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    throw "Frontend dependencies missing. Run npm install in frontend."
}

function Start-ServiceWindow($title, $command) {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "`$Host.UI.RawUI.WindowTitle = '$title'; $command"
    )
}

Start-ServiceWindow "Task 1 - Knowledge Brain" `
    "Set-Location '$root'; & '$python' -m uvicorn main:app --app-dir '$root\task1-knowledge-brain' --host 127.0.0.1 --port 8000"

Start-ServiceWindow "Task 2 - Inbox Agent" `
    "Set-Location '$root'; & '$python' -m uvicorn main:app --app-dir '$root\task2-inbox-agent' --host 127.0.0.1 --port 8001"

Start-ServiceWindow "Task 3 - Meeting to Scope" `
    "Set-Location '$root'; & '$python' -m uvicorn main:app --app-dir '$root\task3-meeting-to-scope' --host 127.0.0.1 --port 8002"

Start-ServiceWindow "AI Consultant Frontend" `
    "Set-Location '$frontend'; npm run dev -- --host 127.0.0.1"

Write-Host "Startup commands sent. Check all four windows for errors."
Write-Host "Task 1: http://127.0.0.1:8000/docs"
Write-Host "Task 2: http://127.0.0.1:8001/docs"
Write-Host "Task 3: http://127.0.0.1:8002/docs"
Write-Host "Frontend: http://127.0.0.1:5173/"
