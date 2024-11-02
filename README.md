# setup + run
recommended: install uv
uv sync
uv run main.py

alternative: pyenv
pyenv install
pyenv activate

less recommended: whatever python is installed

then:
pip install -r requirements.txt
python main.py
