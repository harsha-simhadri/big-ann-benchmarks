#!/bin/bash

import sys
import t3eval

print("Creating competition json...")
t3eval.initialize_competition_json("competition2021.json")

print("Creating baseline config...")
evaluator = t3eval.Evaluator(   "FAISS_GPU_Baseline",
                                "eval_2021/faiss_t3/public_focused.csv",
                                "competition2021.json",
                                system_cost=22021.90,
                                is_baseline=True )
evaluator.eval_all(save_path="eval_2021/faiss_t3/FAISS_GPU_baseline_competition_benchmarks_summary.csv")
evaluator.eval_all(save_path="eval_2021/faiss_t3/FAISS_GPU_baseline_competition_benchmarks_summary.png")
evaluator.commit_baseline("baseline2021.json")

