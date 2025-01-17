"""Tests initializing flax modules directly via tyro."""
import jax
import pytest
from flax import linen as nn
from flax.linen import Module  # https://github.com/google/flax/issues/2636
from jax import numpy as jnp

import tyro


class Classifier(nn.Module):
    layers: int
    units: int
    output_dim: int

    @nn.compact
    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:  # type: ignore
        for i in range(self.layers - 1):
            x = nn.Dense(
                self.units,
                kernel_init=nn.initializers.kaiming_normal(),
            )(x)
            x = nn.relu(x)

        x = nn.Dense(
            self.output_dim,
            kernel_init=nn.initializers.xavier_normal(),
        )(x)
        x = nn.sigmoid(x)
        return x


def test_ok():
    network = tyro.cli(
        Classifier,
        args=[
            "--layers",
            "3",
            "--units",
            "8",
            "--output-dim",
            "3",
        ],
    )

    x = jnp.zeros((10, 4))
    params = network.init(jax.random.PRNGKey(0), x)
    assert network.apply(params, x).shape == (10, 3)


def test_missing():
    with pytest.raises(SystemExit):
        tyro.cli(
            Classifier,
            args=[
                "--layers",
                "3",
                "--units",
                "8",
            ],
        )
