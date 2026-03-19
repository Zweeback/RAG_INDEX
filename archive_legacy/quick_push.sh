#!/bin/bash

# ============================================================================
# GITHUB QUICK PUSH - 3 COMMANDS!
# ============================================================================
# 
# WICHTIG: 
# 1. Erstelle ZUERST ein GitHub Repo: https://github.com/new
#    Name: chatgpt-knowledge-base (oder beliebig)
#    NICHT "Initialize with README" anklicken!
#
# 2. Ändere unten DEIN-USERNAME!
#
# 3. Führe dieses Script aus: bash quick_push.sh
#
# ============================================================================

# ÄNDERE HIER DEINEN GITHUB USERNAME!
GITHUB_USERNAME="DEIN-USERNAME"
REPO_NAME="chatgpt-knowledge-base"

# ============================================================================

echo "🚀 GitHub Quick Push"
echo "===================="
echo ""
echo "Target: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Git initialisieren
echo "📦 1/3: Initialisiere Git..."
git init
git add .
git commit -m "Initial commit: RAG System"
echo "✅ Git initialized!"
echo ""

# Remote hinzufügen
echo "🔗 2/3: Verbinde mit GitHub..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git branch -M main
echo "✅ Remote connected!"
echo ""

# Pushen
echo "⬆️  3/3: Pushe zu GitHub..."
git push -u origin main
echo ""

if [ $? -eq 0 ]; then
    echo "🎉 FERTIG!"
    echo ""
    echo "Dein Repo: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
else
    echo "❌ Fehler beim Pushen!"
    echo ""
    echo "Mögliche Ursachen:"
    echo "- Hast du das GitHub Repo erstellt?"
    echo "- Ist GITHUB_USERNAME korrekt?"
    echo "- Hast du Git Credentials konfiguriert?"
fi
