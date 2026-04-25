# Script để setup môi trường Python cho dự án NMCNPM

Write-Host "Kiem tra va tao Virtual Environment (.venv)..."
if (-Not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Da tao xong .venv."
} else {
    Write-Host "Virtual Environment da ton tai."
}

Write-Host "Kich hoat Virtual Environment..."
# Lưu ý: Cần Set-ExecutionPolicy RemoteSigned -Scope CurrentUser nếu gặp lỗi quyền
. .\.venv\Scripts\Activate.ps1

Write-Host "Nang cap pip..."
python -m pip install --upgrade pip

Write-Host "Go bo thu vien docx cu neu ton tai (vi xung dot voi python-docx)..."
pip uninstall -y docx lxml

Write-Host "Cai dat cac thu vien tu requirements.txt..."
pip install -r requirements.txt

Write-Host "----------------------------------------------------"
Write-Host "Setup hoan tat! Ban co the chay script:"
Write-Host "python make.py --ui"
