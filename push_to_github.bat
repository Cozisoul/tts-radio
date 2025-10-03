@echo off
echo TTS Radio - Push to GitHub
echo ==========================

echo.
echo Please create a GitHub repository first:
echo 1. Go to https://github.com/new
echo 2. Name it "tts-radio" (or your preferred name)
echo 3. Don't initialize with README, .gitignore, or license
echo 4. Click "Create repository"
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: tts-radio): "

if "%REPO_NAME%"=="" set REPO_NAME=tts-radio

echo.
echo Adding remote origin...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo Done! Your TTS Radio project is now on GitHub!
echo Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
pause
