import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0, os.path.abspath("../../..")
)  # Adds the parent directory to the system path

from litellm.litellm_core_utils.core_helpers import get_litellm_metadata_from_kwargs


def test_get_litellm_metadata_from_kwargs():
    kwargs = {
        "litellm_params": {
            "litellm_metadata": {},
            "metadata": {"user_api_key": "1234567890"},
        },
    }
    assert get_litellm_metadata_from_kwargs(kwargs) == {"user_api_key": "1234567890"}


def test_add_missing_spend_metadata_to_litellm_metadata():
    litellm_metadata = {"test_key": "test_value"}
    metadata = {"user_api_key_hash_value": "1234567890"}
    kwargs = {
        "litellm_params": {
            "litellm_metadata": litellm_metadata,
            "metadata": metadata,
        },
    }
    assert get_litellm_metadata_from_kwargs(kwargs) == {
        "test_key": "test_value",
        "user_api_key_hash_value": "1234567890",
    }


def test_preserve_upstream_non_openai_attributes():
    from litellm.litellm_core_utils.core_helpers import (
        preserve_upstream_non_openai_attributes,
    )
    from litellm.types.utils import ModelResponseStream

    model_response = ModelResponseStream(
        id="123",
        object="text_completion",
        created=1715811200,
        model="gpt-3.5-turbo",
    )

    setattr(model_response, "test_key", "test_value")
    preserve_upstream_non_openai_attributes(
        model_response=ModelResponseStream(),
        original_chunk=model_response,
    )

    assert model_response.test_key == "test_value"
