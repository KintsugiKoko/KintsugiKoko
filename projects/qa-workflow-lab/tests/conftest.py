"""Tests use local evidence and injected transports, never a live service."""

import socket

import pytest


@pytest.fixture(autouse=True)
def isolate_network_and_credentials(monkeypatch):
    def reject_network(*args, **kwargs):
        raise AssertionError("Live network access is forbidden in the test suite.")

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.setattr(socket, "create_connection", reject_network)
    monkeypatch.setattr(socket.socket, "connect", reject_network)
    monkeypatch.setattr(socket.socket, "connect_ex", reject_network)
