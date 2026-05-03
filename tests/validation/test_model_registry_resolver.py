from unittest.mock import MagicMock, patch

import pytest

from ml.registry.resolve_model import resolve_model_run_id


def test_resolve_model_run_id_returns_run_id():
    mock_model_version = MagicMock()
    mock_model_version.run_id = "run-123"

    with patch("ml.registry.resolve_model.MlflowClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get_model_version_by_alias.return_value = mock_model_version
        mock_client_class.return_value = mock_client

        run_id = resolve_model_run_id(
            registered_model_name="lumina-rec-movielens-mf",
            model_alias="approved",
            tracking_uri="http://localhost:5000",
        )

    assert run_id == "run-123"


def test_resolve_model_run_id_raises_when_run_id_missing():
    mock_model_version = MagicMock()
    mock_model_version.run_id = None

    with patch("ml.registry.resolve_model.MlflowClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client.get_model_version_by_alias.return_value = mock_model_version
        mock_client_class.return_value = mock_client

        with pytest.raises(ValueError, match="No run ID found"):
            resolve_model_run_id(
                registered_model_name="lumina-rec-movielens-mf",
                model_alias="approved",
                tracking_uri="http://localhost:5000",
            )