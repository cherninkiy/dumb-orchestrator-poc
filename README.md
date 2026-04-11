# dumb-orchestrator-poc
Minimal POC of "dumb orchestrator – smart model". LLM evolves itself by writing plugins (add_plugin/run_plugin). Inspired by MemPalace (96.6% on LongMemEval) and Claude Code's TAOR. Core is immutable (&lt;150 loc). HTTP transport as a plugin.


# Dumb Orchestrator – Smart Model

**Глупый оркестратор, умная модель**  
Минималистичный POC агента, который эволюционирует через плагины, создаваемые самой LLM.

## Идея

Вместо того чтобы зашивать сложность в код, мы даём модели всего два инструмента:
- `add_plugin(name, code)` — написать и сохранить новый плагин
- `run_plugin(name, input_data)` — вызвать существующий плагин

Ядро (оркестратор) — неизменяемый, «глупый» (~150 строк). Вся интеллектуальная работа, включая создание новых возможностей, координацию агентов, память, парсинг данных, — ложится на LLM. Модель сама решает, когда и какой плагин написать, и может перезаписывать их на лету (горячая замена).

## Вдохновение

- **MemPalace / Милла Йовович** — подход, который разнёс LongMemEval (96.6%) без сложного RAG, просто дав модели сырые данные и свободу.
- **Claude Code** — архитектура TAOR (Think‑Act‑Observe‑Repeat) и принцип «глупый оркестратор».
- **Критика переусложнённых RAG‑пайплайнов** — даём модели чистый контекст и право решать.

## Статус

✅ **Реализовано** — ядро, HTTP‑плагин, тесты и CI доступны в ветке [`copilot/core-architecture`](https://github.com/cherninkiy/dumb-orchestrator-poc/tree/copilot/core-architecture).

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Создать .env с ключом Anthropic
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 3. Запустить оркестратор (HTTP-сервер на порту 8080)
python run.py

# 4. Отправить запрос
curl -X POST http://localhost:8080/ \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Напиши плагин, который возвращает текущее время", "context": {}}'
```

Порт сервера можно переопределить через переменную окружения `HTTP_PORT`.

## ⚠️ Предупреждение о безопасности

> **Плагины выполняются с теми же привилегиями, что и сам оркестратор.**  
> Код плагина имеет полный доступ к файловой системе, сети и переменным окружения процесса.  
> **Не запускайте плагины из ненадёжных источников в продакшн-среде.**  
> Этот проект является исследовательским POC — запускайте его только в изолированном окружении (sandbox, Docker, VM).

> **Plugins run with the same privileges as the orchestrator.**  
> Plugin code has unrestricted access to the filesystem, network, and process environment.  
> **Do not load plugins from untrusted sources in a production environment.**  
> This project is a research POC — run it only inside an isolated environment (sandbox, Docker, VM).

## Архитектура

```
dumb-orchestrator-poc/
├── core/
│   ├── plugin_manager.py  # Загрузка/горячая замена плагинов (thread-safe)
│   ├── llm_client.py      # Обёртка Anthropic API с tool use
│   ├── tool_executor.py   # Маршрутизация вызовов инструментов
│   ├── taor_loop.py       # Цикл Think→Act→Observe→Repeat
│   └── utils.py           # Вспомогательные утилиты
├── plugins/
│   └── http.py            # HTTP-транспорт (порт задаётся через HTTP_PORT)
├── system_prompt.txt      # Системный промпт для LLM
└── run.py                 # Точка входа
```

## Лицензия

MIT — свободно используйте идеи, форкайте, улучшайте.

---

*Pull Request: [#1 feat: implement Dumb Orchestrator – Smart Model POC](https://github.com/cherninkiy/dumb-orchestrator-poc/pull/1)*