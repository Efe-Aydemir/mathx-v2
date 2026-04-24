"""
Anti-MathX — Dataset Generation & Validation Utility

Tools for expanding and validating the training dataset.

Usage:
  python generate_dataset.py validate           # Validate existing dataset
  python generate_dataset.py stats              # Show category distribution
  python generate_dataset.py add                # Add a new entry interactively
  python generate_dataset.py template           # Print a blank template
  python generate_dataset.py export-formatted   # Export in Qwen chat template format
"""

import json
import sys
from pathlib import Path
from collections import Counter


DEFAULT_DATASET = Path(__file__).parent.parent / "data" / "dataset.jsonl"
DEFAULT_FORMATTED = Path(__file__).parent.parent / "data" / "dataset_formatted.jsonl"

BASE_INSTRUCTION = (
    "Sen bir matematik profesörüsün. Verilen problemi adım adım, "
    "Chain of Thought yöntemiyle çöz. Her adımı Türkçe açıkla ve "
    "matematiksel ifadeleri LaTeX formatında yaz."
)

# Valid categories and subcategories
CATEGORIES = {
    "Soyut Matematik": [
        "Denklik Bağıntısı",
        "Kısmi Sıralama Bağıntısı",
        "İkili İşlemler",
        "Gruplar",
        "Halkalar",
    ],
    "Lineer Cebir": [
        "Vektör Uzayları",
        "Alt Vektör Uzayları",
        "Determinant",
        "Lineer Dönüşümler",
        "Lineer Birleşim",
    ],
    "Çizge Teorisi": ["Çizge Teorisi"],
    "Topoloji": ["Topoloji"],
}


def load_dataset(path: Path = DEFAULT_DATASET) -> list[dict]:
    """Load all entries from the JSONL file."""
    entries = []
    if not path.exists():
        print(f"❌ Dataset not found: {path}")
        return entries

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def save_dataset(entries: list[dict], path: Path = DEFAULT_DATASET):
    """Save entries back to the JSONL file."""
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✅ Saved {len(entries)} entries to {path}")


def extract_category_info(entry: dict) -> tuple[str, str]:
    """Extract category and subcategory from an entry's input field."""
    input_text = entry.get("input", "")
    if input_text.startswith("[") and "]" in input_text:
        tag = input_text[1:input_text.index("]")]
        parts = tag.split(" - ", 1)
        category = parts[0].strip()
        subcategory = parts[1].strip() if len(parts) > 1 else ""
        return category, subcategory
    return "Unknown", "Unknown"


# ──────────────────────────────────────
# Commands
# ──────────────────────────────────────

def cmd_validate():
    """Validate the dataset for quality and consistency."""
    entries = load_dataset()
    if not entries:
        return

    errors = []
    warnings = []

    for idx, entry in enumerate(entries):
        # Required fields
        for field in ["instruction", "input", "output"]:
            if field not in entry:
                errors.append(f"#{idx}: Missing field '{field}'")
            elif not entry[field].strip():
                errors.append(f"#{idx}: Empty field '{field}'")

        # Input format
        if "input" in entry and not entry["input"].startswith("["):
            errors.append(f"#{idx}: Input should start with [Category - Subcategory]")

        # LaTeX presence in output
        if "output" in entry:
            output = entry["output"]
            if "$" not in output and "$$" not in output:
                warnings.append(f"#{idx}: Output has no LaTeX expressions")
            if "Adım" not in output and "adım" not in output:
                warnings.append(f"#{idx}: Output has no step indicators (Adım)")
            if "Sonuç" not in output and "sonuç" not in output:
                warnings.append(f"#{idx}: Output has no conclusion (Sonuç)")

        # Category validation
        cat, sub = extract_category_info(entry)
        if cat not in CATEGORIES:
            errors.append(f"#{idx}: Unknown category '{cat}'")
        elif sub and sub not in CATEGORIES[cat]:
            warnings.append(f"#{idx}: Unknown subcategory '{sub}' in '{cat}'")

        # Length checks
        if "output" in entry and len(entry["output"]) < 200:
            warnings.append(f"#{idx}: Output is very short ({len(entry['output'])} chars)")

    # Report
    print(f"\n📋 Validation Report for {len(entries)} entries")
    print("=" * 50)

    if errors:
        print(f"\n❌ {len(errors)} Errors:")
        for e in errors:
            print(f"   {e}")
    else:
        print("\n✅ No errors found!")

    if warnings:
        print(f"\n⚠️  {len(warnings)} Warnings:")
        for w in warnings:
            print(f"   {w}")
    else:
        print("✅ No warnings!")

    print()


def cmd_stats():
    """Show category/subcategory distribution."""
    entries = load_dataset()
    if not entries:
        return

    cat_counter = Counter()
    subcat_counter = Counter()

    for entry in entries:
        cat, sub = extract_category_info(entry)
        cat_counter[cat] += 1
        subcat_counter[f"{cat} → {sub}"] += 1

    print(f"\n📊 Dataset Statistics ({len(entries)} total entries)")
    print("=" * 55)

    print("\nCategories:")
    for cat, count in sorted(cat_counter.items()):
        bar = "█" * count
        print(f"  {cat:<20} {count:>3}  {bar}")

    print("\nSubcategories:")
    for subcat, count in sorted(subcat_counter.items()):
        print(f"  {subcat:<45} {count:>3}")

    # Coverage analysis
    print("\n📋 Coverage Analysis:")
    for cat, subcats in CATEGORIES.items():
        for sub in subcats:
            key = f"{cat} → {sub}"
            count = subcat_counter.get(key, 0)
            status = "✅" if count >= 3 else "⚠️ " if count >= 1 else "❌"
            print(f"  {status} {key}: {count}")

    avg_output_len = sum(len(e.get("output", "")) for e in entries) / len(entries)
    print(f"\nAverage output length: {avg_output_len:.0f} chars")
    print()


def cmd_add():
    """Add a new entry interactively."""
    print("\n➕ Add New Training Example")
    print("=" * 40)

    # Category selection
    print("\nCategories:")
    cats = list(CATEGORIES.keys())
    for i, cat in enumerate(cats, 1):
        print(f"  {i}. {cat}")

    try:
        cat_idx = int(input("\nSelect category (number): ")) - 1
        category = cats[cat_idx]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return

    # Subcategory selection
    subcats = CATEGORIES[category]
    print(f"\nSubcategories for {category}:")
    for i, sub in enumerate(subcats, 1):
        print(f"  {i}. {sub}")

    try:
        sub_idx = int(input("Select subcategory (number): ")) - 1
        subcategory = subcats[sub_idx]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return

    # Question
    print(f"\nEnter the question (for [{category} - {subcategory}]):")
    question = input("> ").strip()
    if not question:
        print("❌ Question cannot be empty.")
        return

    # Solution
    print("\nEnter the solution (multi-line, end with an empty line):")
    solution_lines = []
    while True:
        line = input()
        if line == "":
            if solution_lines:
                break
        solution_lines.append(line)

    solution = "\n".join(solution_lines)

    # Build entry
    entry = {
        "instruction": BASE_INSTRUCTION,
        "input": f"[{category} - {subcategory}] Soru: {question}",
        "output": solution,
    }

    # Confirm
    print(f"\n--- Preview ---")
    print(f"Category: {category} - {subcategory}")
    print(f"Question: {question[:80]}...")
    print(f"Solution: {len(solution)} chars")
    confirm = input("\nSave? (y/n): ").strip().lower()

    if confirm == "y":
        entries = load_dataset()
        entries.append(entry)
        save_dataset(entries)
    else:
        print("Cancelled.")


def cmd_template():
    """Print a blank template for manual dataset entry."""
    template = {
        "instruction": BASE_INSTRUCTION,
        "input": "[CATEGORY - SUBCATEGORY] Soru: YOUR QUESTION HERE",
        "output": "## Çözüm\n\n**Verilen:** ...\n\n**Adım 1: ...**\n\n...\n\n**Sonuç:** ... ✅",
    }

    print("\n📝 JSONL Template (copy and fill in):\n")
    print(json.dumps(template, ensure_ascii=False, indent=2))

    print("\n\nValid Categories and Subcategories:")
    for cat, subcats in CATEGORIES.items():
        for sub in subcats:
            print(f"  [{cat} - {sub}]")
    print()


def cmd_export_formatted():
    """Export dataset in Qwen chat template format."""
    entries = load_dataset()
    if not entries:
        return

    template = """<|im_start|>system
{instruction}<|im_end|>
<|im_start|>user
{input}<|im_end|>
<|im_start|>assistant
{output}<|im_end|>"""

    formatted = []
    for entry in entries:
        text = template.format(
            instruction=entry["instruction"],
            input=entry["input"],
            output=entry["output"],
        )
        cat, _ = extract_category_info(entry)
        formatted.append({"text": text, "category": cat})

    save_dataset(formatted, DEFAULT_FORMATTED)
    print(f"✅ Exported {len(formatted)} formatted entries to {DEFAULT_FORMATTED}")


# ──────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────

COMMANDS = {
    "validate": cmd_validate,
    "stats": cmd_stats,
    "add": cmd_add,
    "template": cmd_template,
    "export-formatted": cmd_export_formatted,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Anti-MathX Dataset Utility")
        print(f"\nUsage: python {sys.argv[0]} <command>\n")
        print("Commands:")
        for name, func in COMMANDS.items():
            print(f"  {name:<20} {func.__doc__.strip()}")
        print()
        sys.exit(0)

    COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
