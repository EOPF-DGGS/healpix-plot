# healpix-plotting

_Visualise HEALPix gridded data on geographic map projections._

```{toctree}
---
maxdepth: 2
caption: User guide
hidden: true
---
installation
user-guide/index
tutorials/index
```

```{toctree}
---
maxdepth: 2
caption: Reference
hidden: true
---
api
terminology
```

**healpix-plotting** bridges the [HEALPix](https://healpix.jpl.nasa.gov/) discrete sphere partition
with Matplotlib and Cartopy. It handles resampling and rendering so you can go from a HEALPix array
to a finished map in a single function call.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Tutorials
:link: tutorials/index
:link-type: doc
Step-by-step notebooks: from your first global map to RGB composites and regional subsets.
:::

:::{grid-item-card} API Reference
:link: api
:link-type: doc
Complete documentation for every public function and class.
:::

::::
