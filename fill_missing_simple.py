#!/usr/bin/env python3
"""
Simple version that fills missing results for working models only
"""
import json
import sys
import os
import time

# Load environment
os.chdir(os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment loaded")
except ImportError:
    print("Using system environment")

sys.path.append('./benchmark')
from benchmark import benchmark_question
from get_args import DEFAULT_THRESHOLDS

# Target models that might work (avoiding known problematic ones)
TARGET_MODELS = [
    'mistralai/mistral-saba-25.02',  # These get mapped to working models
    'mistralai/mistral-small-3.1',
    'mistralai/magistral-small', 
    'mistralai/magistral-medium'
]

def main():
    with open('results.json') as f:
        data = json.load(f)
    
    filled_count = 0
    total_attempts = 0
    
    for model_name, temps in data.get('models', {}).items():
        if model_name not in TARGET_MODELS:
            continue
            
        print(f"\n=== Processing {model_name} ===")
        
        for temp_str, qdict in temps.items():
            for question, answers in qdict.items():
                if not answers:  # Empty result
                    total_attempts += 1
                    print(f"Filling {model_name} temp={temp_str} question='{question[:40]}...'")
                    
                    try:
                        new_answers = benchmark_question(
                            question,
                            model_name,
                            float(temp_str),
                            [],
                            chain_of_thought=False,
                            use_llm=False,
                            thresholds=DEFAULT_THRESHOLDS
                        )
                        
                        if new_answers:
                            data["models"][model_name][temp_str][question] = new_answers
                            filled_count += 1
                            print(f"✓ Filled successfully ({len(new_answers)} answers)")
                        else:
                            print("✗ No answers returned")
                            
                        # Save progress every 5 fills
                        if filled_count % 5 == 0:
                            with open('results.json', 'w') as f:
                                json.dump(data, f, indent=2)
                            print(f"Progress saved: {filled_count}/{total_attempts}")
                        
                        time.sleep(2)  # Rate limiting
                        
                    except Exception as e:
                        print(f"✗ Error: {e}")
                        continue
    
    # Final save
    with open('results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nCompleted: {filled_count}/{total_attempts} results filled")

if __name__ == "__main__":
    main()