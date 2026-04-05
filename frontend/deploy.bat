@echo off
echo Starting git deployment > git_log.txt
git init >> git_log.txt 2>&1
git add . >> git_log.txt 2>&1
git commit -m "Ban FE hoan thien ket noi API Render" >> git_log.txt 2>&1
git branch -M main >> git_log.txt 2>&1
git remote add origin git@github.com:ManhAu1111/pet-ai-web.git >> git_log.txt 2>&1
git remote -v >> git_log.txt 2>&1
git push -u origin main >> git_log.txt 2>&1
echo DONE >> git_log.txt
