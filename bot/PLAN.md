# Bot Development Plan

## Overview

This document outlines the development plan for the LMS Telegram Bot. The bot provides students with access to their learning management system (LMS) data through natural language commands and queries.

## Architecture

The bot follows a **testable handler architecture** where command logic is separated from the Telegram transport layer. This enables:

1. **Offline testing** via `--test` mode without Telegram API calls
2. **Unit testing** of handlers without mocking Telegram
3. **Clean separation of concerns** between transport and business logic

## Scaffold Structure

```
bot/
├── bot.py              # Entry point with CLI argument parsing
├── config.py           # Configuration from environment variables
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start command handler
│   ├── help.py         # /help command handler
│   ├── health.py       # /health command handler
│   └── scores.py       # /scores command handler
├── services/
│   ├── __init__.py
│   ├── lms_client.py   # LMS API client
│   └── llm_client.py   # LLM API client for natural language
└── pyproject.toml      # Bot dependencies
```

## Development Phases

### Phase 1: Scaffold (Current)
- Create directory structure with handlers and services
- Implement `--test` mode in `bot.py`
- Add placeholder handlers that return static responses
- Configure `pyproject.toml` with dependencies

### Phase 2: Backend Integration
- Implement `LmsClient` service for API communication
- Connect handlers to real backend endpoints
- Add error handling and retry logic
- Implement authentication flow

### Phase 3: Intent Routing
- Add natural language processing via LLM
- Route user queries to appropriate handlers
- Implement context-aware responses
- Add conversation state management

### Phase 4: Deployment
- Configure Docker integration
- Set up environment variables on VM
- Add health checks and monitoring
- Document deployment procedure

## Testing Strategy

All handlers are pure functions that receive input and return responses. This allows:
- Unit tests without Telegram mocks
- Integration tests with fake LMS client
- End-to-end tests in `--test` mode before deployment

## Deployment

The bot runs as a systemd service on the VM, reading secrets from `.env.bot.secret`. The `docker-compose.yml` will be updated to include the bot service alongside backend and frontend.
