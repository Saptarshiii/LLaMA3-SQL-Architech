import os
import streamlit as st
from typing import Optional

# Delay torch import so the app can start and show informative errors instead of crashing on import.
torch = None
TORCH_IMPORT_ERROR = None
try:
    import torch
except Exception as e:
    TORCH_IMPORT_ERROR = e

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


@st.cache_resource
def load_tokenizer(base_model: str, local_files_only: bool = False):
    return AutoTokenizer.from_pretrained(base_model, local_files_only=local_files_only, use_fast=True)


@st.cache_resource
def load_model(base_model: str, adapter_path: Optional[str], dtype: Optional[str] = "float16", local_files_only: bool = False):
    """Load base model then attach PEFT adapter if `adapter_path` is provided.

    Returns: (model, device)
    """
    if TORCH_IMPORT_ERROR is not None:
        raise RuntimeError(f"Failed to import torch: {TORCH_IMPORT_ERROR}")

    # Determine torch dtype
    torch_dtype = getattr(torch, dtype) if dtype in ("float16", "float32", "bfloat16") else torch.float16

    # Try to load base model (allow local-only for offline use)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype=torch_dtype,
        local_files_only=local_files_only,
        trust_remote_code=True,
    )

    if adapter_path:
        # Wrap with PEFT adapter
        model = PeftModel.from_pretrained(model, adapter_path, local_files_only=local_files_only)

    # Get device for tensors
    try:
        device = next(model.parameters()).device
    except StopIteration:
        device = torch.device("cpu")

    return model, device


def format_prompt(schema: str, question: str) -> str:
    """A simple prompt template the fine-tuned model should understand.

    If your finetuning used a different template, adjust this function accordingly.
    """
    prompt = (
        "### SQL schema:\n"
        f"{schema.strip()}\n\n"
        "### Task:\n"
        "Given the SQL schema above, write an appropriate SQL query for the question.\n\n"
        "### Question:\n"
        f"{question.strip()}\n\n"
        "### SQL:\n"
    )
    return prompt


def generate_sql(model, tokenizer, device, prompt: str, max_new_tokens: int = 256, temperature: float = 0.0, top_p: float = 0.95):
    if TORCH_IMPORT_ERROR is not None:
        raise RuntimeError(f"Failed to import torch: {TORCH_IMPORT_ERROR}")

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=temperature > 0,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Exclude prompt portion and decode
    out = tokenizer.decode(generated[0], skip_special_tokens=True)
    # If model echoes the prompt, try to strip it
    if prompt.strip() and out.startswith(prompt.strip()):
        out = out[len(prompt.strip()):].strip()
    return out


def main():
    st.set_page_config(page_title="Llama SQL - Streamlit UI", layout="wide")
    st.title("Llama SQL — Query generator (Streamlit)")

    st.sidebar.header("Model settings")
    base_model = st.sidebar.text_input("Base model (HF id or local path)", value="meta-llama/Llama-3.2-3B")
    adapter_path = st.sidebar.text_input("Adapter / finetuned folder (path)", value="llama3")
    local_only = st.sidebar.checkbox("Load from local files only", value=True)
    dtype = st.sidebar.selectbox("torch dtype", options=["float16", "float32", "bfloat16"], index=0)

    st.sidebar.markdown("---")
    st.sidebar.markdown("Generation settings")
    max_new_tokens = st.sidebar.slider("max_new_tokens", min_value=16, max_value=2048, value=256)
    temperature = st.sidebar.slider("temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    top_p = st.sidebar.slider("top_p", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

    st.markdown("Provide the database schema (DDL or brief table descriptions) and a natural-language question. The model will generate a SQL query.")

    schema = st.text_area("SQL schema / table definitions", height=200)
    question = st.text_input("Question (in plain English)")

    # If torch failed to import, show a helpful error block but allow the user to read suggestions.
    if TORCH_IMPORT_ERROR is not None:
        st.error("PyTorch failed to import. See the details and recommended fixes in the panel below.")
        with st.expander("Import error details and fixes"):
            st.write(str(TORCH_IMPORT_ERROR))
            st.markdown("**Recommended quick fixes:**\n- Install the Microsoft Visual C++ Redistributable (2015-2022 x64).\n- If you installed a CUDA-enabled torch but don't have matching CUDA/drivers, install the CPU wheel or the correct CUDA build.\n- Set your Windows Power Plan to **High performance** and (for NVIDIA) set Power Management Mode to **Prefer maximum performance** in NVIDIA Control Panel.\n- If you want, I can make the app try a CPU-only import path or give commands to reinstall a CPU-only torch.")

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Load model"):
            with st.spinner("Loading tokenizer and model (this can take a while)..."):
                try:
                    tokenizer = load_tokenizer(base_model, local_files_only=local_only)
                    model, device = load_model(base_model, adapter_path if adapter_path else None, dtype=dtype, local_files_only=local_only)
                    st.success(f"Model loaded on {device}")
                    st.session_state["tokenizer"] = tokenizer
                    st.session_state["model"] = model
                    st.session_state["device"] = device
                except Exception as e:
                    st.error(f"Failed to load model: {e}")

    with c2:
        if st.button("Generate SQL"):
            if "model" not in st.session_state or "tokenizer" not in st.session_state:
                st.warning("Please load the model first using 'Load model' button in the left column.")
            elif not schema.strip() or not question.strip():
                st.warning("Please provide both a schema and a question.")
            else:
                prompt = format_prompt(schema, question)
                with st.spinner("Generating SQL..."):
                    try:
                        out = generate_sql(st.session_state["model"], st.session_state["tokenizer"], st.session_state["device"], prompt, max_new_tokens=max_new_tokens, temperature=temperature, top_p=top_p)
                        st.subheader("Generated SQL")
                        st.code(out)
                    except Exception as e:
                        st.error(f"Generation failed: {e}")

    st.markdown("---")
    st.markdown("Notes:\n- If the model is large, prefer running on a machine with a GPU.\n- If using Hugging Face Hub model IDs that require authentication, set the HF token via environment variable `HF_TOKEN` or configure locally.")


if __name__ == "__main__":
    main()
