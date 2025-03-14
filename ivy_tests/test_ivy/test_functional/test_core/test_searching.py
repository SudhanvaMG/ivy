"""Collection of tests for searching functions."""

# Global
import hypothesis.extra.numpy as hnp
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy.functional.backends.numpy as ivy_np
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# Helpers #
############


@st.composite
def _dtype_x_limited_axis(draw, *, allow_none=False):
    dtype, x, shape = draw(
        helpers.dtype_and_values(
            available_dtypes=helpers.get_dtypes("float"),
            min_num_dims=1,
            min_dim_size=1,
            ret_shape=True,
        )
    )
    if allow_none and draw(st.booleans()):
        return dtype, x, None

    axis = draw(helpers.ints(min_value=0, max_value=len(shape) - 1))
    return dtype, x, axis


@st.composite
def _broadcastable_trio(draw):
    dtype = draw(st.sampled_from(ivy_np.valid_numeric_dtypes))

    shapes_st = hnp.mutually_broadcastable_shapes(num_shapes=3, min_dims=1, min_side=1)
    cond_shape, x1_shape, x2_shape = draw(shapes_st).input_shapes
    cond = draw(hnp.arrays(hnp.boolean_dtypes(), cond_shape))
    x1 = draw(hnp.arrays(dtype, x1_shape))
    x2 = draw(hnp.arrays(dtype, x2_shape))
    return cond, x1, x2, dtype


# Functions #
#############


@handle_cmd_line_args
@given(
    dtype_x_axis=_dtype_x_limited_axis(allow_none=True),
    keepdims=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="argmax"),
)
def test_argmax(
    *,
    dtype_x_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="argmax",
        x=np.asarray(x, dtype=input_dtype),
        axis=axis,
        keepdims=keepdims,
    )


@handle_cmd_line_args
@given(
    dtype_x_axis=_dtype_x_limited_axis(allow_none=True),
    keepdims=st.booleans(),
    num_positional_args=helpers.num_positional_args(fn_name="argmin"),
)
def test_argmin(
    *,
    dtype_x_axis,
    keepdims,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x, axis = dtype_x_axis
    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="argmin",
        x=np.asarray(x, dtype=input_dtype),
        axis=axis,
        keepdims=keepdims,
    )


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("integer", full=True),
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
    ),
    num_positional_args=helpers.num_positional_args(fn_name="nonzero"),
)
def test_nonzero(
    *,
    dtype_and_x,
    as_variable,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    input_dtype, x = dtype_and_x
    helpers.test_function(
        input_dtypes=input_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="nonzero",
        x=np.asarray(x, dtype=input_dtype),
    )


@handle_cmd_line_args
@given(
    broadcastables=_broadcastable_trio(),
    num_positional_args=helpers.num_positional_args(fn_name="where"),
)
def test_where(
    *,
    broadcastables,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
):
    cond, x1, x2, dtype = broadcastables

    helpers.test_function(
        input_dtypes=["bool", dtype, dtype],
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="where",
        condition=cond,
        x1=x1,
        x2=x2,
    )


# indices_where
@handle_cmd_line_args
@given(
    x=helpers.dtype_and_values(available_dtypes=(ivy_np.bool,)),
    num_positional_args=helpers.num_positional_args(fn_name="indices_where"),
)
def test_indices_where(
    *,
    x,
    with_out,
    as_variable,
    num_positional_args,
    native_array,
    container,
    instance_method,
    device,
    fw,
):
    dtype, x = x
    helpers.test_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container,
        instance_method=instance_method,
        fw=fw,
        fn_name="indices_where",
        x=np.asarray(x, dtype=dtype),
    )
