#!/bin/zsh
# デモ実行: 3本のテストを、各操作の前に 1.5 秒止めながら順に流す
cd "$(dirname "$0")"
export AX_SLOW=${AX_SLOW:-1.5}
for t in test_textedit.py test_print_dialog.py test_iprintscan.py; do
  echo "=============================="
  echo "▶ $t"
  echo "=============================="
  ./.venv/bin/python "$t" || { echo "✗ $t FAILED"; exit 1; }
  sleep 2
done
echo "すべて PASS"
