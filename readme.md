```
# Активировать окружение
source venv/bin/activate
```

``` # создать суперюзера
DJANGO_SUPERUSER_PASSWORD=secret123 \
python3 src/manage.py createsuperuser \
    --noinput \
    --username admin \
    --email admin@example.com
```

# создать группу волонтеров
```
python3 src/manage.py create_volunteer_group
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
