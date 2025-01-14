import tensorflow as tf

from tavolo.seq2vec import YangAttention


def test_shapes():
    """ Test input-output shapes """

    # Inputs shape
    input_shape_3d = (56, 10, 30)
    attention_units = 100

    inputs_3d = tf.random.normal(shape=input_shape_3d)

    yang_attention = YangAttention(n_units=attention_units,
                                   name='yang_attention')

    output = yang_attention(inputs_3d)

    # Assert correctness of output shapes
    assert output.shape == (input_shape_3d[0], input_shape_3d[-1])


def test_masking():
    """ Test masking support """

    # Input
    input_shape_3d = (56, 10, 30)
    attention_units = 100
    inputs_3d = tf.random.normal(shape=input_shape_3d)
    mask = tf.less(tf.reduce_sum(tf.reduce_sum(inputs_3d, axis=-1), axis=-1), 0)
    masked_input = tf.where(mask, tf.zeros_like(inputs_3d), inputs_3d)

    # Layers
    masking_layer = tf.keras.layers.Masking(mask_value=0., input_shape=input_shape_3d[1:])
    yang_attention = YangAttention(n_units=attention_units,
                                   name='yang_attention')

    result = yang_attention(masking_layer(masked_input))

    assert result.shape == (input_shape_3d[0], input_shape_3d[-1])
