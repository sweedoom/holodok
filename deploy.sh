#!/usr/bin/env bash
# Создаёт/обновляет репозиторий и пушит. Нужен GitHub CLI (`gh auth login`).
set -e

cd "$(dirname "$0")"

# параметры репо — поправь на свои
REPO=${REPO:-sweedoom/holodok}   # на github.com/USER/REPO
COMMIT="site update $(date +%Y-%m-%d-%H%M)"

# проверка сборки
python build.py

# init / remote
if [ ! -d .git ]; then
  git init -q -b main
fi
git add -A
if git diff --cached --quiet; then
  echo "нечего коммитить — всё уже на месте"
  exit 0
fi
git -c user.name=site-bot -c user.email=bot@local commit -q -m "$COMMIT"

# создать репо, если его нет
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  echo "создаю репозиторий $REPO"
  gh repo create "$REPO" --public --source=. --remote=origin --push
else
  if ! git remote get-url origin >/dev/null 2>&1; then
    gh repo edit "$REPO" --add-remote origin || true
    REM=$(gh repo view "$REPO" --json url -q .url)
    git remote add origin "$REM"
  fi
  git push -u origin main
fi

# включить Pages на /docs (нужно для репо, у которого ещё не включено)
OWNER=$(gh repo view "$REPO" --json owner -q .owner.login)
NAME=$(gh repo view "$REPO" --json name -q .name)
gh api "repos/$OWNER/$NAME/pages" -X POST \
  -f "source[branch]=main" -f "source[path]=/docs" >/dev/null 2>&1 || true

USER_LOGIN=$(gh api user -q .login)
echo
echo "✓ запушено. Сайт появится через 1-2 минуты на:"
echo "  https://${USER_LOGIN}.github.io/${NAME}/"