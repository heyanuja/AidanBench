#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append('./benchmark')

from benchmark import benchmark_question
from get_args import DEFAULT_THRESHOLDS
import time

def debug_full_benchmark():
    print("Testing full benchmark_question with timeouts...")
    print(f"Thresholds: {DEFAULT_THRESHOLDS}")
    
    start_time = time.time()
    try:
        result = benchmark_question(
            'What is 2+2?',
            'x-ai/grok-3-mini-beta:medium',
            0.7,
            [],
            chain_of_thought=False,
            use_llm=False,
            thresholds=DEFAULT_THRESHOLDS
        )
        elapsed = time.time() - start_time
        print(f"SUCCESS after {elapsed:.1f}s: Got {len(result)} answers")
        for i, ans in enumerate(result):
            print(f"  Answer {i+1}: coherence={ans['coherence_score']}, dissim={ans['embedding_dissimilarity_score']:.3f}")
    
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"ERROR after {elapsed:.1f}s: {e}")

if __name__ == "__main__":
    debug_full_benchmark()