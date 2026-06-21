#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append('./benchmark')

from prompts import gen_answer, judge_answer
from models import embed
import numpy as np

def debug_benchmark_question(question, model_name):
    print(f"Step 1: Generate answer for {model_name}")
    try:
        new_answer = gen_answer(question, [], model_name, False)
        print(f"✓ Generated: {new_answer[:50]}...")
    except Exception as e:
        print(f"✗ gen_answer failed: {e}")
        return
    
    print(f"Step 2: Judge answer")
    try:
        coherence_score = judge_answer(question, new_answer, model_name='o1-mini')
        print(f"✓ Coherence score: {coherence_score}")
    except Exception as e:
        print(f"✗ judge_answer failed: {e}")
        return
    
    print(f"Step 3: Get embedding")
    try:
        embedding = embed(new_answer)
        print(f"✓ Embedding: {len(embedding)} dimensions")
    except Exception as e:
        print(f"✗ embed failed: {e}")
        return
    
    print("✓ All steps completed successfully!")

if __name__ == "__main__":
    debug_benchmark_question("What is 2+2?", "x-ai/grok-3-mini-beta:medium")