"""
Dataset preparation script for Qwen2.5-Math fine-tuning.
Reads the JSONL dataset, validates entries, and formats them
with the Qwen2.5 chat template for training.
"""

import json
import sys
from pathlib import Path


PROMPT_TEMPLATE = """<|im_start|>system
{instruction}<|im_end|>
<|im_start|>user
{input}<|im_end|>
<|im_start|>assistant
{output}<|im_end|>"""


def validate_entry(entry: dict, idx: int) -> list[str]:
    """Validate a single dataset entry and return list of errors."""
    errors = []
    required_fields = ["instruction", "input", "output"]
    
    for field in required_fields:
        if field not in entry:
            errors.append(f"Entry {idx}: Missing required field '{field}'")
        elif not entry[field].strip():
            errors.append(f"Entry {idx}: Empty field '{field}'")
    
    if "input" in entry:
        # Check that input contains category tag
        if not entry["input"].startswith("["):
            errors.append(f"Entry {idx}: Input should start with [Category - Subcategory] tag")
    
    if "output" in entry:
        # Check for LaTeX content
        if "$$" not in entry["output"] and "$" not in entry["output"]:
            errors.append(f"Entry {idx}: Output should contain LaTeX math expressions")
    
    return errors


def format_entry(entry: dict) -> str:
    """Format a dataset entry using the Qwen2.5 chat template."""
    return PROMPT_TEMPLATE.format(
        instruction=entry["instruction"],
        input=entry["input"],
        output=entry["output"],
    )


def prepare_dataset(input_path: str, output_path: str):
    """Read, validate, and format the dataset."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    entries = []
    all_errors = []
    
    with open(input_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"Entry {idx}: Invalid JSON - {e}")
                continue
            
            errors = validate_entry(entry, idx)
            all_errors.extend(errors)
            
            formatted = {
                "text": format_entry(entry),
                "category": entry.get("input", "").split("]")[0].replace("[", "").strip(),
            }
            entries.append(formatted)
    
    # Report
    print(f"Total entries: {len(entries)}")
    print(f"Validation errors: {len(all_errors)}")
    
    if all_errors:
        print("\nErrors:")
        for error in all_errors:
            print(f"  - {error}")
    
    # Category distribution
    categories = {}
    for entry in entries:
        cat = entry["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Write output
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"\nFormatted dataset written to: {output_path}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "../data/dataset.jsonl"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "../data/dataset_formatted.jsonl"
    prepare_dataset(input_path, output_path)
