# Git Freeze and Commit Commands

Run these locally inside the repository.

```bash
git status
git add assignments_frozen/ docs/ report/ protocols/ environment/ README_final_tasks.md
git commit -m "Freeze HW1-HW3 experimental assignment versions"
git rev-parse HEAD
```

Copy the output hash into `freeze_commit_hash.txt`.

After the nine controlled trials and evidence upload are complete:

```bash
git status
git add evidence/ results.csv previous_experiments_inventory.csv environment/ freeze_commit_hash.txt README_final_tasks.md
git commit -m "Add controlled ChatGPT trial evidence and final manuscript materials"
git rev-parse HEAD
```

Send the final hash to the professor.
