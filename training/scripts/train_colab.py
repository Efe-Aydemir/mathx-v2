"""
Anti-MathX — Qwen2.5-Math-7B Fine-Tuning Script (Unsloth + LoRA)

This script can run:
  1. On Google Colab (free T4 GPU)
  2. On any Linux machine with an NVIDIA GPU

Usage — Google Colab:
  Upload this file to Colab, then run:
    !pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
    !pip install --no-deps trl peft accelerate bitsandbytes xformers
    %run train_colab.py

Usage — Local / RunPod:
  pip install "unsloth @ git+https://github.com/unslothai/unsloth.git"
  pip install trl peft accelerate bitsandbytes
  python train_colab.py --dataset-path ../data/dataset.jsonl
"""

import argparse
import json
import os
import sys
from pathlib import Path


# ──────────────────────────────────────
# 1. Parse arguments
# ──────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Anti-MathX Qwen2.5-Math fine-tuning with Unsloth LoRA"
    )
    parser.add_argument(
        "--dataset-path",
        type=str,
        default="../data/dataset.jsonl",
        help="Path to the raw JSONL dataset",
    )
    parser.add_argument(
        "--config-path",
        type=str,
        default="../configs/training_config.yaml",
        help="Path to training_config.yaml",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="../outputs",
        help="Directory to save LoRA adapters",
    )
    parser.add_argument(
        "--push-to-hub",
        action="store_true",
        help="Push the trained model to HuggingFace Hub",
    )
    parser.add_argument(
        "--hub-model-id",
        type=str,
        default="",
        help="HuggingFace Hub model ID (e.g. username/anti-mathx-qwen)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Override number of training epochs",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=None,
        help="Override learning rate",
    )
    return parser.parse_args()


# ──────────────────────────────────────
# 2. Load config
# ──────────────────────────────────────

def load_config(config_path: str) -> dict:
    """Load training configuration from YAML file."""
    try:
        import yaml
    except ImportError:
        print("⚠️  PyYAML not found, using default config.")
        return {}

    config_file = Path(config_path)
    if not config_file.exists():
        print(f"⚠️  Config file not found: {config_path}, using defaults.")
        return {}

    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ──────────────────────────────────────
# 3. Prepare dataset
# ──────────────────────────────────────

CHAT_TEMPLATE = """<|im_start|>system
{instruction}<|im_end|>
<|im_start|>user
{input}<|im_end|>
<|im_start|>assistant
{output}<|im_end|>"""


def load_and_format_dataset(dataset_path: str) -> list[dict]:
    """Load the JSONL dataset and format each entry with the Qwen chat template."""
    entries = []
    path = Path(dataset_path)

    if not path.exists():
        # Try relative to this script's location
        script_dir = Path(__file__).parent
        path = script_dir / dataset_path
        if not path.exists():
            print(f"❌ Dataset not found: {dataset_path}")
            sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"⚠️  Skipping line {idx}: {e}")
                continue

            text = CHAT_TEMPLATE.format(
                instruction=entry["instruction"],
                input=entry["input"],
                output=entry["output"],
            )
            entries.append({"text": text})

    print(f"✅ Loaded {len(entries)} training examples from {path}")
    return entries


# ──────────────────────────────────────
# 4. Main training loop
# ──────────────────────────────────────

def main():
    args = parse_args()
    config = load_config(args.config_path)

    # Extract config sections with defaults
    model_cfg = config.get("model", {})
    lora_cfg = config.get("lora", {})
    train_cfg = config.get("training", {})

    # Model parameters
    model_name = model_cfg.get("name", "unsloth/Qwen2.5-Math-7B")
    max_seq_length = model_cfg.get("max_seq_length", 8192)
    load_in_4bit = model_cfg.get("load_in_4bit", True)

    # LoRA parameters
    lora_r = lora_cfg.get("r", 32)
    lora_alpha = lora_cfg.get("lora_alpha", 16)
    lora_dropout = lora_cfg.get("lora_dropout", 0)
    target_modules = lora_cfg.get("target_modules", [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ])
    use_gradient_checkpointing = lora_cfg.get("use_gradient_checkpointing", "unsloth")

    # Training parameters (CLI overrides config)
    epochs = args.epochs or train_cfg.get("num_train_epochs", 3)
    lr = args.lr or train_cfg.get("learning_rate", 2e-4)
    batch_size = train_cfg.get("per_device_train_batch_size", 2)
    grad_accum = train_cfg.get("gradient_accumulation_steps", 4)
    warmup_steps = train_cfg.get("warmup_steps", 10)
    logging_steps = train_cfg.get("logging_steps", 10)
    save_steps = train_cfg.get("save_steps", 100)
    optim = train_cfg.get("optim", "adamw_8bit")
    weight_decay = train_cfg.get("weight_decay", 0.01)
    lr_scheduler = train_cfg.get("lr_scheduler_type", "linear")
    seed = train_cfg.get("seed", 42)
    output_dir = args.output_dir or train_cfg.get("output_dir", "../outputs")

    # ── Print config ──
    print("\n" + "=" * 60)
    print("  🧮 Anti-MathX — Fine-Tuning Pipeline")
    print("=" * 60)
    print(f"  Model:         {model_name}")
    print(f"  4-bit:         {load_in_4bit}")
    print(f"  Max Seq Len:   {max_seq_length}")
    print(f"  LoRA r:        {lora_r}, alpha: {lora_alpha}")
    print(f"  Epochs:        {epochs}")
    print(f"  Batch Size:    {batch_size} (grad accum: {grad_accum})")
    print(f"  Learning Rate: {lr}")
    print(f"  Output Dir:    {output_dir}")
    print("=" * 60 + "\n")

    # ── Step 1: Load model ──
    print("📦 Step 1/4: Loading model...")
    try:
        from unsloth import FastLanguageModel
    except ImportError:
        print("❌ Unsloth is not installed!")
        print("   Colab:  !pip install 'unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git'")
        print("   Local:  pip install 'unsloth @ git+https://github.com/unslothai/unsloth.git'")
        sys.exit(1)

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=None,  # Auto-detect
        load_in_4bit=load_in_4bit,
    )
    print("✅ Model loaded successfully.\n")

    # ── Step 2: Add LoRA adapters ──
    print("🔧 Step 2/4: Adding LoRA adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        target_modules=target_modules,
        bias="none",
        use_gradient_checkpointing=use_gradient_checkpointing,
        random_state=seed,
        use_rslora=False,
        loftq_config=None,
    )

    # Print trainable parameters
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"✅ LoRA adapters added. Trainable: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)\n")

    # ── Step 3: Prepare dataset ──
    print("📊 Step 3/4: Preparing dataset...")
    formatted_data = load_and_format_dataset(args.dataset_path)

    from datasets import Dataset
    dataset = Dataset.from_list(formatted_data)
    print(f"✅ Dataset ready: {len(dataset)} examples\n")

    # ── Step 4: Train ──
    print("🚀 Step 4/4: Starting training...")

    from trl import SFTTrainer
    from transformers import TrainingArguments

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        num_train_epochs=epochs,
        learning_rate=lr,
        warmup_steps=warmup_steps,
        logging_steps=logging_steps,
        save_steps=save_steps,
        save_total_limit=3,
        optim=optim,
        weight_decay=weight_decay,
        lr_scheduler_type=lr_scheduler,
        seed=seed,
        fp16=True,
        bf16=False,
        report_to="none",  # Disable wandb / tensorboard
        dataloader_pin_memory=True,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        args=training_args,
        packing=True,  # Pack multiple short examples into one sequence
    )

    # GPU stats before training
    try:
        import torch
        if torch.cuda.is_available():
            gpu_stats = torch.cuda.get_device_properties(0)
            print(f"   GPU: {gpu_stats.name}")
            print(f"   VRAM: {gpu_stats.total_mem / 1024**3:.1f} GB")
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"   Reserved: {reserved:.1f} GB")
    except Exception:
        pass

    print()
    trainer_stats = trainer.train()

    # ── Results ──
    print("\n" + "=" * 60)
    print("  ✅ Training Complete!")
    print("=" * 60)
    print(f"  Total Steps:    {trainer_stats.global_step}")
    print(f"  Training Loss:  {trainer_stats.training_loss:.4f}")
    print(f"  Runtime:        {trainer_stats.metrics.get('train_runtime', 0):.0f}s")
    print("=" * 60)

    # ── Save model ──
    print(f"\n💾 Saving LoRA adapters to: {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("✅ LoRA adapters saved.\n")

    # ── Optional: Push to Hub ──
    if args.push_to_hub and args.hub_model_id:
        print(f"📤 Pushing to HuggingFace Hub: {args.hub_model_id}")
        try:
            model.push_to_hub(args.hub_model_id, tokenizer=tokenizer)
            print(f"✅ Pushed to: https://huggingface.co/{args.hub_model_id}")
        except Exception as e:
            print(f"⚠️  Hub push failed: {e}")
            print("   You can push manually later with merge_lora.py --push-to-hub")

    # ── Quick test ──
    print("\n🧪 Quick test with a sample question:")
    FastLanguageModel.for_inference(model)

    test_input = """<|im_start|>system
Sen bir matematik profesörüsün. Verilen problemi adım adım, Chain of Thought yöntemiyle çöz. Her adımı Türkçe açıkla ve matematiksel ifadeleri LaTeX formatında yaz.<|im_end|>
<|im_start|>user
[Lineer Cebir - Determinant] Soru: 2x2 birim matrisin determinantını bulunuz.<|im_end|>
<|im_start|>assistant
"""

    inputs = tokenizer(test_input, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.3,
        top_p=0.9,
        do_sample=True,
    )
    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    print(response[:500])
    print("\n✅ All done! Next steps:")
    print(f"   1. Merge LoRA:  python merge_lora.py --lora-path {output_dir}")
    print(f"   2. Deploy:      bash deploy_vllm.sh merged-model/")
    print(f"   3. API:         Set MOCK_MODE=false in api/.env\n")


if __name__ == "__main__":
    main()
