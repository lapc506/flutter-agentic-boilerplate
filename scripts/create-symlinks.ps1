# Script para crear symlinks de skills a diferentes herramientas
# Uso: .\scripts\create-symlinks.ps1

# Requiere ejecución como administrador en Windows
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  Este script requiere permisos de administrador para crear symlinks en Windows" -ForegroundColor Yellow
    Write-Host "Ejecuta PowerShell como administrador y vuelve a intentar" -ForegroundColor Yellow
    exit 1
}

# Obtener la ruta del proyecto (raíz del repo)
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$SkillsDir = Join-Path $ProjectRoot "skills"

Write-Host "📦 Creando symlinks desde skills/ hacia diferentes herramientas..." -ForegroundColor Cyan
Write-Host "Proyecto: $ProjectRoot" -ForegroundColor Gray
Write-Host "Skills: $SkillsDir" -ForegroundColor Gray
Write-Host ""

# 1. Cursor Rules (.cursor/rules/)
$CursorRulesDir = Join-Path $ProjectRoot ".cursor" "rules"
if (-not (Test-Path $CursorRulesDir)) {
    New-Item -ItemType Directory -Path $CursorRulesDir -Force | Out-Null
    Write-Host "✅ Creado: $CursorRulesDir" -ForegroundColor Green
}

$CursorSymlink = Join-Path $CursorRulesDir "skills"
if (Test-Path $CursorSymlink) {
    Write-Host "⚠️  Ya existe: $CursorSymlink" -ForegroundColor Yellow
    Remove-Item $CursorSymlink -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType SymbolicLink -Path $CursorSymlink -Target $SkillsDir | Out-Null
Write-Host "✅ Symlink creado: $CursorSymlink -> $SkillsDir" -ForegroundColor Green

# 2. Kiro Steering (.kilocode/rules/)
$KiroRulesDir = Join-Path $ProjectRoot ".kilocode" "rules"
if (-not (Test-Path $KiroRulesDir)) {
    New-Item -ItemType Directory -Path $KiroRulesDir -Force | Out-Null
    Write-Host "✅ Creado: $KiroRulesDir" -ForegroundColor Green
}

$KiroSymlink = Join-Path $KiroRulesDir "skills"
if (Test-Path $KiroSymlink) {
    Write-Host "⚠️  Ya existe: $KiroSymlink" -ForegroundColor Yellow
    Remove-Item $KiroSymlink -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType SymbolicLink -Path $KiroSymlink -Target $SkillsDir | Out-Null
Write-Host "✅ Symlink creado: $KiroSymlink -> $SkillsDir" -ForegroundColor Green

# 3. Claude Project Skills (.claude/skills/)
$ClaudeSkillsDir = Join-Path $ProjectRoot ".claude" "skills"
if (-not (Test-Path $ClaudeSkillsDir)) {
    New-Item -ItemType Directory -Path $ClaudeSkillsDir -Force | Out-Null
    Write-Host "✅ Creado: $ClaudeSkillsDir" -ForegroundColor Green
}

# Crear symlinks para cada skill individual
$SkillsSubdirs = Get-ChildItem -Path $SkillsDir -Directory
foreach ($SkillDir in $SkillsSubdirs) {
    $SkillName = $SkillDir.Name
    $ClaudeSkillSymlink = Join-Path $ClaudeSkillsDir $SkillName
    
    if (Test-Path $ClaudeSkillSymlink) {
        Write-Host "⚠️  Ya existe: $ClaudeSkillSymlink" -ForegroundColor Yellow
        Remove-Item $ClaudeSkillSymlink -Force -ErrorAction SilentlyContinue
    }
    
    New-Item -ItemType SymbolicLink -Path $ClaudeSkillSymlink -Target $SkillDir.FullName | Out-Null
    Write-Host "✅ Symlink creado: $ClaudeSkillSymlink -> $($SkillDir.FullName)" -ForegroundColor Green
}

# 4. Gemini CLI Extensions (~/.gemini/extensions/)
$GeminiExtensionsDir = Join-Path $env:USERPROFILE ".gemini" "extensions"
if (-not (Test-Path $GeminiExtensionsDir)) {
    New-Item -ItemType Directory -Path $GeminiExtensionsDir -Force | Out-Null
    Write-Host "✅ Creado: $GeminiExtensionsDir" -ForegroundColor Green
}

# Crear una extensión "flutter-agent-skills" que apunta a todo el directorio skills
$GeminiExtensionName = "flutter-agent-skills"
$GeminiExtensionDir = Join-Path $GeminiExtensionsDir $GeminiExtensionName
if (Test-Path $GeminiExtensionDir) {
    Write-Host "⚠️  Ya existe: $GeminiExtensionDir" -ForegroundColor Yellow
    Remove-Item $GeminiExtensionDir -Force -Recurse -ErrorAction SilentlyContinue
}
New-Item -ItemType SymbolicLink -Path $GeminiExtensionDir -Target $SkillsDir | Out-Null
Write-Host "✅ Symlink creado: $GeminiExtensionDir -> $SkillsDir" -ForegroundColor Green

# Crear gemini-extension.json si no existe
$GeminiExtensionJson = Join-Path $GeminiExtensionDir "gemini-extension.json"
if (-not (Test-Path $GeminiExtensionJson)) {
    $ExtensionJson = @{
        name = "flutter-agent-skills"
        version = "1.0.0"
        description = "Flutter Agent Skills - Comprehensive collection of Flutter development skills"
        author = "Flutter Agent Skills Team"
        repository = "https://github.com/your-org/flutter-agent-skills"
    } | ConvertTo-Json -Depth 10
    
    # Como es un symlink, necesitamos crear el JSON en el directorio real
    $ExtensionJsonPath = Join-Path $SkillsDir "gemini-extension.json"
    $ExtensionJson | Out-File -FilePath $ExtensionJsonPath -Encoding UTF8
    Write-Host "✅ Creado: gemini-extension.json" -ForegroundColor Green
}

# 5. OpenAI Codex (codex/skills/)
$CodexSkillsDir = Join-Path $ProjectRoot "codex" "skills"
if (-not (Test-Path $CodexSkillsDir)) {
    New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null
    Write-Host "✅ Creado: $CodexSkillsDir" -ForegroundColor Green
}

# Crear symlinks para cada skill individual
foreach ($SkillDir in $SkillsSubdirs) {
    $SkillName = $SkillDir.Name
    $CodexSkillSymlink = Join-Path $CodexSkillsDir $SkillName
    
    if (Test-Path $CodexSkillSymlink) {
        Write-Host "⚠️  Ya existe: $CodexSkillSymlink" -ForegroundColor Yellow
        Remove-Item $CodexSkillSymlink -Force -ErrorAction SilentlyContinue
    }
    
    New-Item -ItemType SymbolicLink -Path $CodexSkillSymlink -Target $SkillDir.FullName | Out-Null
    Write-Host "✅ Symlink creado: $CodexSkillSymlink -> $($SkillDir.FullName)" -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ ¡Symlinks creados exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Resumen:" -ForegroundColor Cyan
Write-Host "  • Cursor Rules: .cursor/rules/skills" -ForegroundColor Gray
Write-Host "  • Kiro Steering: .kilocode/rules/skills" -ForegroundColor Gray
Write-Host "  • Claude Skills: .claude/skills/*" -ForegroundColor Gray
Write-Host "  • Gemini Extensions: ~/.gemini/extensions/flutter-agent-skills" -ForegroundColor Gray
Write-Host "  • OpenAI Codex: codex/skills/*" -ForegroundColor Gray
Write-Host ""

