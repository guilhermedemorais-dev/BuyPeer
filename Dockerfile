FROM php:8.2-apache

ENV APACHE_DOCUMENT_ROOT=/var/www/html/public

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        unzip \
        zip \
        libfreetype6-dev \
        libicu-dev \
        libjpeg62-turbo-dev \
        libonig-dev \
        libpng-dev \
        libxml2-dev \
        libzip-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j"$(nproc)" \
        bcmath \
        exif \
        gd \
        intl \
        mbstring \
        opcache \
        pdo_mysql \
        soap \
        zip \
    && a2enmod rewrite headers expires \
    && sed -ri "s!/var/www/html!${APACHE_DOCUMENT_ROOT}!g" /etc/apache2/sites-available/*.conf /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

COPY composer.json composer.lock ./
RUN composer install \
    --no-dev \
    --prefer-dist \
    --optimize-autoloader \
    --no-interaction \
    --no-progress \
    --no-scripts

COPY . .

RUN chmod +x docker/start-container.sh \
    && mkdir -p \
        bootstrap/cache \
        storage/app/public \
        storage/framework/cache \
        storage/framework/sessions \
        storage/framework/views \
        storage/logs \
    && chown -R www-data:www-data bootstrap/cache storage

ENTRYPOINT ["docker/start-container.sh"]
CMD ["apache2-foreground"]
