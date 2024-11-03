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

---

mkdir -p 'data/10k/'
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf'
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/lyft_2021.pdf' -O 'data/10k/lyft_2021.pdf'
