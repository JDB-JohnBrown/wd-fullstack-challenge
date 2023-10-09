start .\frontend\install.bat
cd backend
pip install virtualenv
python -m virtualenv .env
.\.env\Scripts\pip.exe install -r requirements.txt

