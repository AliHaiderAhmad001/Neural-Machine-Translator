# -*- coding: utf-8 -*-
"""encoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iAjbOC_0Y8t2SafAmfKp29Dkrn-7T56q
"""

import tensorflow as tf
from attention import AttentionHead, MultiHead_Attention
from feed_forward import FeedForward

class Encoder(tf.keras.layers.Layer):
    """
    Encoder layer implementation.

    Args:
        config: Configuration object.

    Attributes:
        multihead_attention: Multi-head attention layer.
        norm1: Layer normalization layer.
        norm2: Layer normalization layer.
        feed_forward: Feed-forward layer.
        dropout: Dropout layer.
    """

    def __init__(self, config, name=None, **kwargs):
        super(Encoder, self).__init__(name=name)
        super(Encoder, self).__init__(**kwargs)
        self.supports_masking = True
        self.multihead_attention = MultiHead_Attention(config)
        self.norm1 = tf.keras.layers.LayerNormalization()
        self.norm2 = tf.keras.layers.LayerNormalization()
        self.feed_forward = FeedForward(config)
        self.dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)

    def call(self, hidden_state, mask=None, training=False):
        """
        Applies the encoder layer to the input hidden state.

        Args:
            hidden_state: Hidden state tensor (bs, len, dim).
            mask: Padding mask tensor (bs, len, len) or (bs, 1, len) or None.
            training: Boolean flag indicating whether the layer is in training mode or not.

        Returns:
            Updated hidden state after applying the encoder layer.
        """

        attention_output = self.multihead_attention(hidden_state, hidden_state, hidden_state, mask = None)  # Apply multi-head attention
        hidden_state = self.norm1(attention_output + hidden_state)  # Add skip connection and normalize
        feed_forward_output = self.feed_forward(hidden_state)  # Apply feed-forward layer
        hidden_state = self.norm2(feed_forward_output + hidden_state)  # Add skip connection and normalize
        hidden_state = self.dropout(hidden_state, training=training)  # Apply dropout
        return hidden_state

    def get_config(self):
        """
        Returns the configuration of the encoder layer.

        Returns:
            Configuration dictionary.
        """

        config = super().get_config()
        config.update({
            "multihead_attention": self.multihead_attention,
            "norm1": self.norm1,
            "norm2": self.norm2,
            "feed_forward": self.feed_forward,
            "dropout": self.dropout,
        })
        return config