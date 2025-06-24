# RDM Workshop Kit - Penguins Dataset

This repository contains a modified version of the [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) dataset as a [DataLad](https://www.datalad.org/) dataset.
These data are referenced in examples and used alongside the [mix-and-match modules](https://hub.datalad.org/edu/slides) for research data management (RDM) workshops.

## How to use

With DataLad installed, clone the dataset:

```
datalad clone https://hub.datalad.org/edu/palmerpenguins.git
```

Get all subdatasets:

```
datalad get -r .
```

Retrieve required content, e.g., images, via

```
datalad get <path>
```

## Dataset structure

- [adelie/](./adelie): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Adélie penguins (Pygoscelis adeliae) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) dataset
- [chinstrap/](./chinstrap): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Chinstrap penguins (Pygoscelis antarcticus) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e) dataset
- [gentoo/](./gentoo): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Gentoo penguin (Pygoscelis papua) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689) dataset
- [portal.edirepository.org/](./portal.edirepository.org): Archives from the source data package download URLs accessed from the [Environmental Data Initiative (EDI) Data Portal](https://portal.edirepository.org/nis/home.jsp)
