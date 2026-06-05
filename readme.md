```
# Активировать окружение
source venv/bin/activate
```

```
# Запустить проект
python3 src/manage.py runserver 0.0.0.0:8001
```

# для промптов
```
DIR="${1:-.}"
OUT="all_files.txt"

: > "$OUT"

find "$DIR" -type f | while read -r file; do
    if file "$file" | grep -q 'text'; then
        echo "===== $file =====" >> "$OUT"
        cat "$file" >> "$OUT"
        printf "\n\n" >> "$OUT"
    fi
done
```