# Penguins Dataset

This repository brings penguins of all sorts into the world of Distributed Data Management with DataLad.

It contains:
- precurated data archives and associated metadata from the study [Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis)](https://doi.org/10.1371/journal.pone.0090081) by Kristen B Gorman and coauthors, along with all the data files extracted from these archives
- images from [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page) of the three different species of penguin (Adélie, Chinstrap, and Gentoo) that are represented in the study data
- helper scripts and files for (meta)data transformation

All of this content is wrapped together as a [DataLad](https://www.datalad.org/) dataset that serves to demonstrate the (meta)data handling capabilities of tools in the DataLad ecosystem. The dataset is referenced in examples and used alongside the [mix-and-match modules](https://hub.datalad.org/edu/slides) for Research Data Management (RDM) workshops.

## Use the dataset

With DataLad installed, clone the dataset:

```
datalad clone https://hub.datalad.org/edu/palmerpenguins.git
```

Retrieve required content, e.g., images, via

```
datalad get <path>
```

Please refer to [LICENSE.txt](LICENSE.txt) for content-specific sharing and usage terms.

## Structure of main content

- [portal.edirepository.org/](./portal.edirepository.org): Archives from the source data package download URLs accessed from the [Environmental Data Initiative (EDI) Data Portal](https://portal.edirepository.org/nis/home.jsp)
- [adelie/](./adelie): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Adélie penguins (Pygoscelis adeliae) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) dataset
- [chinstrap/](./chinstrap): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Chinstrap penguins (Pygoscelis antarcticus) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e) dataset
- [gentoo/](./gentoo): Extracted contents from full data package for [Structural size measurements and isotopic signatures of foraging among adult male and female Gentoo penguin (Pygoscelis papua) nesting along the Palmer Archipelago near Palmer Station, 2007-2009](https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689) dataset
- [examples/](./examples): Penguin images from Wikimedia Commons


# Acknowledgements

The formation of this dataset was largely inspired by the [`palmerpenguins` R-package and dataset](https://allisonhorst.github.io/palmerpenguins/index.html) that were created (from the same study and data sources) by Allison Marie Horst, Alison Presmanes Hill, and Kristen B Gorman.

Thanks go also to Wikimedia Commmons users `Nanosmile` and `Godot13` for sharing the penguin images.

# References

- Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis). PLoS ONE 9(3):e90081. https://doi.org/10.1371/journal.pone.0090081
- Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data. R package version 0.1.0. https://allisonhorst.github.io/palmerpenguins/. doi: 10.5281/zenodo.3960218.
- Palmer Station Antarctica LTER and K. Gorman, 2020. Structural size measurements and isotopic signatures of foraging among adult male and female Adélie penguins (Pygoscelis adeliae) nesting along the Palmer Archipelago near Palmer Station, 2007-2009 ver 5. Environmental Data Initiative. https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f.
- Palmer Station Antarctica LTER and K. Gorman, 2020. Structural size measurements and isotopic signatures of foraging among adult male and female Gentoo penguin (Pygoscelis papua) nesting along the Palmer Archipelago near Palmer Station, 2007-2009 ver 5. Environmental Data Initiative. https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689.
- Palmer Station Antarctica LTER and K. Gorman, 2020. Structural size measurements and isotopic signatures of foraging among adult male and female Chinstrap penguin (Pygoscelis antarcticus) nesting along the Palmer Archipelago near Palmer Station, 2007-2009 ver 6. Environmental Data Initiative. https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e.

