import numpy as np
import pandas as pd

from plotstack import PlotStack
df = EXAMPLE_DATAFRAME = pd.DataFrame({"a": np.arange(10), "b": np.arange(10, 20)})

def test_plotstack_dimensions():
    stack = PlotStack(figure=None, subplot_width=10, subplot_height=3) 
    df = EXAMPLE_DATAFRAME
    df.plot(ax=stack.add_subplot())

    df = df * -1 # Some transformation
    df.plot(ax=stack.add_subplot(height=1))

    df = df * 2 # Some other transformation
    df.plot(ax=stack.add_subplot(height=2))

    assert stack.nrows == 3
    assert sum(stack._subplot_heights) == 6
    assert stack.subplot_width == 10