"""
Script to merge LoRA adapters with the base model after training.
Produces a standalone model ready for vLLM serving.
"""

import sys
from pathlib import Path


def merge_lora(
    base_model: str = "unsloth/Qwen2.5-Math-7B",
    lora_path: str = "outputs",
    output_path: str = "merged-model",
    push_to_hub: bool = False,
    hub_model_id: str = "",
):
    """Merge LoRA adapters with the base model."""
    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("Error: Unsloth is not installed. Run: pip install unsloth")
        sys.exit(1)

    print(f"Loading base model: {base_model}")
    print(f"Loading LoRA from: {lora_path}")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=lora_path,
        max_seq_length=8192,
        load_in_4bit=False,
    )

    # Save merged model locally
    print(f"Merging and saving to: {output_path}")
    model.save_pretrained_merged(
        output_path,
        tokenizer,
        save_method="merged_16bit",
    )

    print(f"✅ Merged model saved to: {output_path}")

    # Optionally push to Hugging Face Hub
    if push_to_hub and hub_model_id:
        print(f"Pushing to Hugging Face Hub: {hub_model_id}")
        model.push_to_hub_merged(
            hub_model_id,
            tokenizer,
            save_method="merged_16bit",
        )
        print(f"✅ Pushed to: https://huggingface.co/{hub_model_id}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merge LoRA adapters with base model")
    parser.add_argument("--base-model", default="unsloth/Qwen2.5-Math-7B")
    parser.add_argument("--lora-path", default="outputs")
    parser.add_argument("--output-path", default="merged-model")
    parser.add_argument("--push-to-hub", action="store_true")
    parser.add_argument("--hub-model-id", default="")

    args = parser.parse_args()
    merge_lora(
        base_model=args.base_model,
        lora_path=args.lora_path,
        output_path=args.output_path,
        push_to_hub=args.push_to_hub,
        hub_model_id=args.hub_model_id,
    )
