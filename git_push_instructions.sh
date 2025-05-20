#!/bin/bash
# Instructions to push your project to GitHub from the current directory

# 1. Initialize git repository (if not already initialized)
git init

# 2. Add all files to staging
git add .

# 3. Commit the changes
git commit -m "Initial commit"

# 4. Add remote repository (replace URL with your GitHub repo URL)
git remote add origin https://github.com/your-username/your-repo.git

# 5. Push to GitHub main branch
git push -u origin main

# Note:
# - Replace https://github.com/your-username/your-repo.git with your actual GitHub repository URL.
# - If your default branch is 'master' instead of 'main', replace 'main' with 'master' in the push command.
