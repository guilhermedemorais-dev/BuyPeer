#!/bin/sh
set -e

cd /var/www/html

mkdir -p \
  bootstrap/cache \
  storage/app/public \
  storage/framework/cache \
  storage/framework/sessions \
  storage/framework/views \
  storage/logs

chown -R www-data:www-data bootstrap/cache storage

php artisan package:discover --ansi || true
php artisan storage:link >/dev/null 2>&1 || true

if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  echo "Waiting for MySQL at ${DB_HOST:-mysql}:${DB_PORT:-3306}..."

  until php -r '
    $host = getenv("DB_HOST") ?: "mysql";
    $port = (int) (getenv("DB_PORT") ?: 3306);
    $database = getenv("DB_DATABASE") ?: "";
    $username = getenv("DB_USERNAME") ?: "";
    $password = getenv("DB_PASSWORD") ?: "";

    try {
        new PDO(
            sprintf("mysql:host=%s;port=%d;dbname=%s", $host, $port, $database),
            $username,
            $password,
            [PDO::ATTR_TIMEOUT => 3]
        );
        exit(0);
    } catch (Throwable $exception) {
        fwrite(STDERR, $exception->getMessage() . PHP_EOL);
        exit(1);
    }
  '; do
    sleep 3
  done

  php artisan migrate --force
fi

php artisan config:cache || true
php artisan route:cache || true
php artisan view:cache || true

exec "$@"
