# Llama SQL — Streamlit UI

This small Streamlit app lets you interactively use your finetuned Llama model (text->SQL). It expects that you have:

- a base model (e.g. `meta-llama/Llama-3.2-3B`) available locally or from the Hugging Face Hub
- your finetuned adapter/weights in a folder (by default the app uses `llama3` — change it in the sidebar)

Files added:
- `app.py` — the Streamlit application
- `requirements.txt` — Python packages required to run the app

How to run (Windows PowerShell):

1. Create and activate a Python environment (example using venv):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```

2. Run Streamlit:

```powershell
streamlit run app.py
```

3. In the app's sidebar set:
- Base model: HF id or local path. Default is `meta-llama/Llama-3.2-3B`.
- Adapter / finetuned folder: path to your finetuned weights (e.g., `llama3` or the `llama3-sql-lora` folder). If your adapter files are stored under `llama3`, set that.
- Toggle `Load from local files only` if you don't want the app to fetch from the Hub.

Notes & tips
- If the model is very large, run on a machine with a GPU and enough VRAM. Device allocation uses `device_map='auto'`.
- If you need to authenticate to Hugging Face Hub, either set `HF_TOKEN` environment variable or use `huggingface-cli login`.
- If your finetuning used a different prompt template, edit `format_prompt` inside `app.py` to match that template for best results.

If you want, I can also:
- Add a small example schema + question to demo the app.
- Add an automated smoke test that loads the tokenizer only (fast) and verifies basic generation.
