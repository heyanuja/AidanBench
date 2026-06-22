#!/usr/bin/env python3
"""
fill_missing_results.py

Rerun any missing questions (empty answer lists) in a benchmark results JSON file.
This covers both CoT and non-CoT runs using the existing benchmark_question logic.

Usage:
  python fill_missing_results.py --file results.json
  python fill_missing_results.py --file results_cot.json --cot
"""
import argparse
import json
import sys
import os

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env")
except ImportError:
    print("python-dotenv not available, using system environment variables")

# Add benchmark directory to path
sys.path.append('./benchmark')

from benchmark import benchmark_question
from get_args import DEFAULT_THRESHOLDS


def main():
    parser = argparse.ArgumentParser(
        description="Fill missing answers in benchmark result JSON"
    )
    parser.add_argument(
        "--file", required=True,
        help="Path to the results JSON file"
    )
    parser.add_argument(
        "--cot", action="store_true",
        help="Use chain-of-thought (CoT) for reruns"
    )
    args = parser.parse_args()

    thresholds = DEFAULT_THRESHOLDS
    use_llm = False

    # Load existing results
    with open(args.file) as f:
        data = json.load(f)

    models = data.get("models", {})
    total_reruns = 0

    # Iterate over model/temp/question and rerun where answers list is empty
    for model_name, temps in models.items():
        for temp_str, qdict in temps.items():
            for question, answers in qdict.items():
                if not answers:
                    # Skip thinking-model entries when not in CoT mode
                    if not args.cot and model_name.endswith(':thinking'):
                        continue
                    
                    # All models should work now with fixed mappings
                        
                    print(f"Re-running model={model_name} temp={temp_str} question='{question}'")
                    try:
                        new_answers = benchmark_question(
                            question,
                            model_name,
                            float(temp_str),
                            [],
                            chain_of_thought=args.cot,
                            use_llm=use_llm,
                            thresholds=thresholds,
                        )
                        data["models"][model_name][temp_str][question] = new_answers
                        total_reruns += 1
                        
                        # Add delay between API calls to avoid rate limiting
                        import time
                        time.sleep(2)  # Increased delay to reduce rate limiting
                        
                    except Exception as e:
                        print(f"Failed to process {model_name}: {str(e)}")
                        # Continue with next model instead of stopping
                        continue

    if total_reruns == 0:
        print(f"No missing answers found in {args.file}.")
    else:
        # Write back updated results
        with open(args.file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Updated {args.file}: reran {total_reruns} missing entries.")


if __name__ == "__main__":
    main()