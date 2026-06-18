# ── Docker / Host networking note ────────────────────────────────────────────
# Ollama must be installed and running on the host machine (not in Docker) at
# http://localhost:11434 by default. Django running inside Docker reaches host
# services via http://host.docker.internal:11434 on Windows/Mac. Linux users
# may need to add extra_hosts: ['host.docker.internal:host-gateway'] to the
# django service in docker-compose.dev.yml.
# ─────────────────────────────────────────────────────────────────────────────

"""
chatbotAPI/services/llm_client.py

Sends chat completion requests to a locally running Ollama instance.
Uses the /api/chat endpoint with the model specified in Django settings.
No API key required — Ollama is completely free and local.
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def complete_chat(system_prompt, user_message, context_json=None):
    """
    Send a chat completion request to the local Ollama instance.

    Parameters
    ----------
    system_prompt : str
        The system-level instruction that sets the assistant's behaviour.
    user_message : str
        The end-user's message / question.
    context_json : dict or None, optional
        Additional context (e.g. current page, schematic data) that will
        be appended to the system prompt as readable text.

    Returns
    -------
    str
        The assistant's reply text.

    Raises
    ------
    ValueError
        With message "OLLAMA_UNAVAILABLE" if Ollama cannot be reached,
        "OLLAMA_TIMEOUT" if the request times out,
        "OLLAMA_MODEL_ERROR" if Ollama returns a non-200 status (e.g.
        the requested model is not pulled locally), or
        "OLLAMA_ERROR: <reason>" for any other failure.
    """
    base_url = settings.OLLAMA_BASE_URL
    model = settings.OLLAMA_MODEL
    url = f"{base_url}/api/chat"

    # Append context to system prompt if provided
    effective_system_prompt = system_prompt
    if context_json:
        effective_system_prompt += (
            "\n\nCurrent circuit context: " + str(context_json)
        )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": effective_system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=30)

        # Detect non-200 responses explicitly (e.g. 404 when the model
        # name in OLLAMA_MODEL has not been pulled locally).
        if response.status_code != 200:
            logger.error(
                "[chatbotAPI] Ollama returned HTTP %d", response.status_code
            )
            raise ValueError("OLLAMA_MODEL_ERROR")

        data = response.json()
        reply = data["message"]["content"]
        return reply.strip()

    except ValueError:
        # Re-raise our own ValueErrors (OLLAMA_MODEL_ERROR) without
        # catching them in the generic handler below.
        raise

    except requests.exceptions.ConnectionError:
        logger.error("[chatbotAPI] Ollama connection failed — is it running?")
        raise ValueError("OLLAMA_UNAVAILABLE")

    except requests.exceptions.Timeout:
        logger.error("[chatbotAPI] Ollama request timed out (30s limit)")
        raise ValueError("OLLAMA_TIMEOUT")

    except Exception as exc:
        logger.error("[chatbotAPI] Ollama error: %s", type(exc).__name__)
        raise ValueError(f"OLLAMA_ERROR: {exc}")
