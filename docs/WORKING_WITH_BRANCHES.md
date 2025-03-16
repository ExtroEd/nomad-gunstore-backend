# Инструкция по работе с ветками Git

Эта инструкция поможет вам эффективно управлять ветками в Git, используя стратегии `main`, `develop` и `feature`.

## Структура веток

- **`main`**: Ветка, которая всегда содержит стабильную, рабочую версию кода. Она готова для продакшена.
- **`develop`**: Ветка для разработки. Все новые фичи и исправления добавляются сюда. Когда фичи готовы, они сливаются с `main`.
- **`feature/название-ветки`**: Ветки для отдельных фич. В них ведется работа над фичей, и они сливаются в `develop`, когда фича готова.

## Работа с веткой для фичи

1. Переключитесь на ветку `develop`:

    ```bash
    git checkout develop
    ```

2. Создайте новую ветку для фичи:

    ```bash
    git checkout -b feature/название-ветки
    ```

    Пример: 

    ```bash
    git checkout -b feature/login-system
    ```

3. Внесите изменения, добавьте файлы и зафиксируйте коммит:

    ```bash
    git add .
    git commit -m "Добавлена логин-система"
    ```

4. Пушьте изменения в удаленную ветку фичи:

    ```bash
    git push origin feature/login-system
    ```

## Слияние ветки фичи в `develop`

1. Переключитесь на ветку `develop`:

    ```bash
    git checkout develop
    ```

2. Слейте ветку фичи в `develop`:

    ```bash
    git merge feature/название-ветки
    ```

3. Разрешите конфликты, если они возникли, и сделайте коммит слияния.

4. Пушьте изменения в `develop`:

    ```bash
    git push origin develop
    ```

## Слияние `develop` в `main` (готовим к продакшену)

1. Переключитесь на ветку `main`:

    ```bash
    git checkout main
    ```

2. Слейте ветку `develop` в `main`:

    ```bash
    git merge develop
    ```

3. Разрешите конфликты, если они возникли, и сделайте коммит слияния.

4. Пушьте изменения в `main`:

    ```bash
    git push origin main
    ```

## Пошаговый пример работы

1. Создание ветки `develop`:

    ```bash
    git checkout main
    git checkout -b develop
    git push origin develop
    ```

2. Создание ветки для фичи:

    ```bash
    git checkout develop
    git checkout -b feature/login-system
    git add .
    git commit -m "Добавлена логин-система"
    git push origin feature/login-system
    ```

3. Слияние ветки фичи в `develop`:

    ```bash
    git checkout develop
    git merge feature/login-system
    git push origin develop
    ```

4. Слияние `develop` в `main`:

    ```bash
    git checkout main
    git merge develop
    git push origin main
    ```

## Заключение

Теперь у вас есть чёткая структура для работы с ветками:

- Используйте ветку `develop` для разработки.
- Работайте над фичами в ветках вида `feature/название-ветки`.
- Сливайте изменения в `develop`, а потом в `main`, когда фичи готовы.

Эта схема поможет вам поддерживать чистоту кода и легко отслеживать прогресс разработки.
