"""
chatbotAPI/tests/test_views.py

Tests for ChatMessageView. All tests mock llm_client.complete_chat so
they run without a real Ollama server (safe for CI/CD).
"""
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class ChatMessageViewTests(TestCase):
    """Tests for POST /api/chat/message/."""

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/chat/message/'

    # ── Test 1: Ollama unavailable → 503 ─────────────────────────────────

    @patch('chatbotAPI.views.complete_chat')
    def test_ollama_unavailable_returns_503(self, mock_chat):
        """When Ollama is unreachable the view must return 503."""
        mock_chat.side_effect = ValueError("OLLAMA_UNAVAILABLE")

        response = self.client.post(
            self.url,
            data={'message': 'What is a resistor?'},
            format='json',
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn('error', response.data)

    # ── Test 2: Empty message → 400 ──────────────────────────────────────

    def test_empty_message_returns_400(self):
        """An empty message field must fail serializer validation (400)."""
        response = self.client.post(
            self.url,
            data={'message': ''},
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    # ── Test 3: Valid message with mocked reply → 200 ────────────────────

    @patch('chatbotAPI.views.complete_chat')
    def test_valid_message_returns_200(self, mock_chat):
        """A valid message with a successful LLM reply returns 200."""
        mock_chat.return_value = "Test reply"

        response = self.client.post(
            self.url,
            data={'message': 'What is a capacitor?'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['reply'], "Test reply")
        self.assertIn('conversation_id', response.data)
        self.assertEqual(response.data['sources'], [])

    # ── Test 4: Whitespace-only message → 400 ────────────────────────────

    def test_whitespace_only_message_returns_400(self):
        """A whitespace-only message must be rejected (400)."""
        response = self.client.post(
            self.url,
            data={'message': '   \n\t  '},
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    # ── Test 5: Model not pulled (OLLAMA_MODEL_ERROR) → 503 ─────────────

    @patch('chatbotAPI.views.complete_chat')
    def test_model_error_returns_503(self, mock_chat):
        """When Ollama returns non-200 (model not pulled) → 503."""
        mock_chat.side_effect = ValueError("OLLAMA_MODEL_ERROR")

        response = self.client.post(
            self.url,
            data={'message': 'Hello'},
            format='json',
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn('error', response.data)
        self.assertIn('ollama pull', response.data['error'])

    # ── Test 6: Timeout → 504 ────────────────────────────────────────────

    @patch('chatbotAPI.views.complete_chat')
    def test_timeout_returns_504(self, mock_chat):
        """When Ollama times out the view must return 504."""
        mock_chat.side_effect = ValueError("OLLAMA_TIMEOUT")

        response = self.client.post(
            self.url,
            data={'message': 'Hello'},
            format='json',
        )

        self.assertEqual(response.status_code, 504)
        self.assertIn('error', response.data)
