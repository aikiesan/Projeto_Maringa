# Sobe o ambiente local e carrega o codebook. Requer Docker Desktop em execução.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "[.env criado a partir de .env.example]" }

docker compose up -d
Write-Host "[aguardando o banco ficar pronto]"
$ok = $false
foreach ($i in 1..40) {
  docker compose exec -T db pg_isready -U maringa -d maringa *> $null
  if ($LASTEXITCODE -eq 0) { $ok = $true; break }
  Start-Sleep -Seconds 2
}
if (-not $ok) { throw "O banco nao respondeu. Veja: docker compose logs db" }

$env:DATABASE_URL = "postgresql://maringa:maringa@localhost:55432/maringa"
python -m database.migrate
python -m tools.load_evidence --all

Write-Host ""
Write-Host "Pronto. Adminer: http://localhost:8080  (servidor: db, usuario: maringa)"
Write-Host "Painel:  abra index.html no navegador, ou rode: python -m tools.build_site"
