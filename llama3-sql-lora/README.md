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

Dataset: the adapter was fine-tuned on a text-to-SQL dataset. Please replace this line with the exact dataset name (for example, Spider or a custom dataset), dataset splits used, preprocessing steps, and any filtering applied.

Training procedure: see `../Notebook/Model Finetuning.ipynb` for code, hyperparameters (batch size, learning rate, number of epochs), optimizer, and compute resources used. If you want, I can extract the training hyperparameters and paste them here.

### Evaluation

Please add metrics used for validation (e.g., exact-match, execution accuracy) and results here. If you ran an evaluation script, include a short table with metrics and the evaluation dataset.

### Licensing & Distribution

If you plan to share this adapter publicly, add an explicit LICENSE file in the repo and ensure any datasets used allow redistribution. `adapter_model.safetensors` is a large binary — track it with Git LFS if pushing to GitHub.

### Contact

Maintainer: Saptarshi Banik


### Model Sources Hugging Face

<!-- Provide the basic links for the model. -->

- **Repository:** [More Information Needed]
- **Paper [optional]:** [More Information Needed]
- **Demo [optional]:** [More Information Needed]

## Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

### Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->

[More Information Needed]

### Downstream Use [optional]

<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->

[More Information Needed]

### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->

[More Information Needed]

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

[More Information Needed]

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

Users (both direct and downstream) should be made aware of the risks, biases and limitations of the model. More information needed for further recommendations.

## How to Get Started with the Model

Use the code below to get started with the model.

[More Information Needed]

## Training Details

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

[More Information Needed]

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Preprocessing [optional]

[More Information Needed]


#### Training Hyperparameters

- **Training regime:** [More Information Needed] <!--fp32, fp16 mixed precision, bf16 mixed precision, bf16 non-mixed precision, fp16 non-mixed precision, fp8 mixed precision -->

#### Speeds, Sizes, Times [optional]

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->

[More Information Needed]

## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

### Testing Data, Factors & Metrics

#### Testing Data

<!-- This should link to a Dataset Card if possible. -->

[More Information Needed]

#### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->

[More Information Needed]

#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

[More Information Needed]

### Results

[More Information Needed]

#### Summary



## Model Examination [optional]

<!-- Relevant interpretability work for the model goes here -->

[More Information Needed]

## Environmental Impact

<!-- Total emissions (in grams of CO2eq) and additional considerations, such as electricity usage, go here. Edit the suggested text below accordingly -->

Carbon emissions can be estimated using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700).

- **Hardware Type:** [More Information Needed]
- **Hours used:** [More Information Needed]
- **Cloud Provider:** [More Information Needed]
- **Compute Region:** [More Information Needed]
- **Carbon Emitted:** [More Information Needed]

## Technical Specifications [optional]

### Model Architecture and Objective

[More Information Needed]

### Compute Infrastructure

[More Information Needed]

#### Hardware

[More Information Needed]

#### Software

[More Information Needed]

## Citation [optional]

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

[More Information Needed]

**APA:**

[More Information Needed]

## Glossary [optional]

<!-- If relevant, include terms and calculations in this section that can help readers understand the model or model card. -->

[More Information Needed]

## More Information [optional]

[More Information Needed]

## Model Card Authors [optional]

[More Information Needed]

## Model Card Contact

[More Information Needed]
### Framework versions

- PEFT 0.12.0