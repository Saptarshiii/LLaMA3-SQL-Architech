---
base_model: meta-llama/Llama-3.2-3B
library_name: peft
---

# Model Card for Model ID

<!-- Provide a quick summary of what the model is/does. -->



## Model Details

### Model Description

<!-- Provide a longer summary of what this model is. -->



- **Developed by:** Saptarshi Banik
- **Funded by [optional]:** self
- **Shared by [optional]:** self
- **Model type:** Text-to-Text
- **Language(s) (NLP):** English
- **License:** self
- **Finetuned from model [optional]:** meta-llama/Llama-3.2-3B

This folder contains a PEFT adapter that was fine-tuned to translate natural-language questions (given a SQL schema) into SQL queries. The adapter is intentionally small compared to the base model and can be attached to the Llama 3 base model using PEFT.

Files included
- `adapter_config.json` — PEFT adapter configuration
- `adapter_model.safetensors` — finetuned adapter weights (safetensors)
- `special_tokens_map.json`, `tokenizer_config.json`, `tokenizer.json` — tokenizer/config artifacts

Known framework versions
- PEFT 0.12.0

### Intended use

This adapter is intended to be used together with the base model `meta-llama/Llama-3.2-3B` to generate SQL queries from natural language questions in the context of a provided schema. Typical downstream use-cases include:

- Prototyping SQL generation for dashboards and analytics tools
- Assisting developers or analysts to quickly produce SQL from questions

Out-of-scope / Limitations
- The model may hallucinate or generate incorrect SQL; outputs must be validated before use in production or destructive queries.\
- The adapter was trained on a specific dataset; results may not generalize to unseen schemas or domains without additional fine-tuning.

### How to load and use (example)

The recommended way to use the adapter is to load the base model and then attach the PEFT adapter. Example (Python):

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model = "meta-llama/Llama-3.2-3B"
adapter_path = "./llama3-sql-lora"

tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=True, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", trust_remote_code=True, local_files_only=True)
model = PeftModel.from_pretrained(model, adapter_path, local_files_only=True)

# Now prepare prompt and generate
prompt = "<your schema and question here>"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Dataset and training details

Dataset: the adapter was fine-tuned on a text-to-SQL dataset "b-mc2/sql-create-context".

Training procedure: see `../Notebook/Model Finetuning.ipynb` for code, hyperparameters (batch size, learning rate, number of epochs), optimizer, and compute resources used. If you want, I can extract the training hyperparameters and paste them here.

### Contact

Maintainer: Saptarshi Banik


### Framework versions

- PEFT 0.12.0
