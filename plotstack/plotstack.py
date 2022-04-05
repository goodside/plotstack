from dataclasses import dataclass, field, astuple
from typing import Any
import matplotlib.pyplot as plt
import matplotlib as mpl


InchSize = int | float


@dataclass
class PlotStack:
    """
    A wrapped `Figure` instance containing a grid of sublots arranged in a
    single column, each with a consistent width. This constrained layout
    simplifies creating subplot layouts through interactive, iteratively written
    notebook code. Plots produced by this class have a consistent width, but a
    height that adapts to the number of subplots and their individual heights.

    Constructor accepts an optional `figure` to wrap. If `figure=None`, a new,
    empty `Figure` is created.
    
    The parameter `subplot_width=10` specifies the fixed width of all subplots
    in inches. The parameter `subplot_height=3` likewise specifies a default
    height, but this can be overridden by the `height=` parameter of
    `add_subplot` for each subplot individually.

    """

    figure: plt.Figure = None
    subplot_width: InchSize = 10
    subplot_height: InchSize = 3
    height_ratios: list[InchSize] = field(init=False)

    def __post_init__(self):
        # Create new `Figure` if needed:
        if self.figure is None:
            self.figure = plt.figure()
        self.height_ratios = []

    @property
    def nrows(self) -> int:
        """Number of rows in the `GridSpec`."""
        try:
            return self.axes[0].get_gridspec().nrows
        except IndexError:  # No `Axes` have been added yet.
            return 0

    def add_subplot(self, height: InchSize = None) -> plt.Axes:
        """
        Append new `Axes` with given `height` to wrapped `Figure`, so that the final
        figure height increases by `height`.  Returns the new `Axes`.
        """

        if height is None:
            height = self.subplot_height
        self.height_ratios.append(height)

        # Set all existing subplot `Axes` to use new, expanded `GridSpec`:
        gs = mpl.gridspec.GridSpec(
            self.nrows + 1, 1, figure=self.figure, height_ratios=self.height_ratios
        )
        for i, ax in enumerate(self.figure.axes):
            ax.set_subplotspec(mpl.gridspec.SubplotSpec(gs, i))

        # Create new subplot `Axes`:
        ax = self.figure.add_subplot(gs.nrows, 1, len(self.axes) + 1)

        self.set_size_inches(self.subplot_width, sum(self.height_ratios))

        # Return newly created `Axes`, mirroring semantics of `Figure.add_subplot`:
        return ax

    def __getattr__(self, attr) -> Any:
        """Forward all attribute requests to the wrapped `Figure`. """
        return getattr(self.figure, attr)
