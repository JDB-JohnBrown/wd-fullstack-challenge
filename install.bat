cd frontend
yarn install
cd ..\backend
python -m ensurepip --upgrade
pip install virtualenv
python -m virtualenv .env
.\.env\Scripts\activate
pip install -r requirements.txt

