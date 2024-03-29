# transformer.py

import tensorflow as tf
from encoder import Encoder
from decoder import Decoder
from embeddings import Embeddings


class Transformer(tf.keras.Model):
    """
    Transformer model implementation for sequence-to-sequence tasks.

    Args:
        config: Configuration object containing model hyperparameters.
        source_vocab_size: The vocabulary size of the source language.
        target_vocab_size: The vocabulary size of the target language.

    Attributes:
        enc_embed_layer: Embeddings layer for the encoder inputs.
        dec_embed_layer: Embeddings layer for the decoder inputs.
        encoder: List of encoder layers.
        decoder: List of decoder layers.
        dropout: Dropout layer for regularization.
        output_layer: Dense layer for output prediction.

    Methods:
        call: Forward pass of the transformer model.
        get_config: Returns the configuration dictionary of the transformer model.
    """

    def __init__(self, config, source_vocab_size, target_vocab_size, name=None, **kwargs):
        super(Transformer, self).__init__(name=name)
        super(Transformer, self).__init__(**kwargs)
        self.enc_embed_layer = Embeddings(config, source_vocab_size)
        self.dec_embed_layer = Embeddings(config, target_vocab_size)
        self.encoder = [Encoder(config) for _ in range(config.num_blocks)]
        self.decoder = [Decoder(config) for _ in range(config.num_blocks)]
        self.dropout = tf.keras.layers.Dropout(config.final_dropout_prob)
        self.output_layer = tf.keras.layers.Dense(target_vocab_size)

    def call(self, inputs, training=False):
        """
        Forward pass of the transformer model.

        Args:
            inputs: Input data.
            training: Boolean flag indicating whether the model is in training mode or not.

        Returns:
            Output logits of the transformer model.
        """
        source_inputs = inputs["encoder_inputs"]
        target_inputs = inputs["decoder_inputs"]

        x_enc = self.enc_embed_layer(source_inputs, training=training)
        x_dec = self.dec_embed_layer(target_inputs, training=training)

        for encoder_layer in self.encoder:
            x_enc = encoder_layer(x_enc, training=training)

        # Remove the mask used in the encoder as it's not needed in the decoder
        x_enc._keras_mask = None

        for decoder_layer in self.decoder:
            x_dec = decoder_layer(x_dec, x_enc, training=training)

        x_dec = self.dropout(x_dec, training=training)
        x_logits = self.output_layer(x_dec)

        # Remove the mask from the logits as it's not needed in the loss function
        x_logits._keras_mask = None

        return x_logits

    def get_config(self):
        """
        Returns the configuration dictionary of the transformer model.

        Returns:
            Configuration dictionary.
        """
        config = super().get_config()
        config.update({
            "enc_embed_layer": self.enc_embed_layer,
            "dec_embed_layer": self.dec_embed_layer,
            "encoder": self.encoder,
            "decoder": self.decoder,
            "dropout": self.dropout,
            "encoder": self.encoder,
            "decoder": self.decoder,
            "output_layer": self.output_layer,
        })
        return config
