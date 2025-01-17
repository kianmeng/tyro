.. Comment: this file is automatically generated by `update_example_docs.py`.
   It should not be modified manually.

JAX/Flax Integration
==========================================


If you use `flax.linen <https://github.com/google/flax>`_\ , modules can be instantiated
directly from ``tyro.cli``.



.. code-block:: python
        :linenos:


        from flax import linen as nn
        from flax.linen import Module  # https://github.com/google/flax/issues/2636
        from jax import numpy as jnp

        import tyro


        class Classifier(Module):
            layers: int
            """Layers in our network."""
            units: int = 32
            """Hidden unit count."""
            output_dim: int = 10
            """Number of classes."""

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


        def train(model: Classifier, num_iterations: int = 1000) -> None:
            """Train a model.

            Args:
                model: Model to train.
                num_iterations: Number of training iterations.
            """
            print(f"{model=}")
            print(f"{num_iterations=}")


        if __name__ == "__main__":
            tyro.cli(train)

------------

.. raw:: html

        <kbd>python 04_additional/07_flax.py --help</kbd>

.. program-output:: python ../../examples/04_additional/07_flax.py --help

------------

.. raw:: html

        <kbd>python 04_additional/07_flax.py --model.layers 4</kbd>

.. program-output:: python ../../examples/04_additional/07_flax.py --model.layers 4
