#!/usr/bin/env python3
import json

with open('results.json') as f:
    data = json.load(f)

empty = sum(1 for temps in data.get('models',{}).values() 
           for questions in temps.values() 
           for q in questions.values() if not q)

print(f'Empty results: {empty}/1768 ({empty/1768*100:.1f}% remaining)')
print(f'Filled results: {1768-empty}/1768 ({(1768-empty)/1768*100:.1f}% complete)')