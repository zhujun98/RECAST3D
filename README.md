# RECAST3D

REConstruction of Arbitrary Slices in Tomography

![](https://raw.githubusercontent.com/cicwi/RECAST3D/develop/docs/preview_usage.gif)

This project contains a full-stack implementation of a tomographic reconstruction and visualization pipeline.

RECAST3D is visualization software for tomographic imaging based on on-demand reconstruction of arbitrary slices, and is built for use in a distributed,
real-time, and online reconstruction pipeline.

The repository also contains two support libraries, *TomoPackets* and *SliceRecon*.

The TomoPackets library defines a protocol for sending messages between the different
components (scanners, reconstruction nodes, visualization workstations) for
real-time tomographic reconstruction and we encourage its use also outside of RECAST3D.

SliceRecon contains efficient implementations for reconstructing
arbitrarily oriented slices through a 3D volume. It defines servers that are
able to communicate to data sources (using TomoPackets) and visualization
software (such as, but not exclusively, RECAST3D).


## Installation

```sh
# On Ra
module load gcc/9.3.0
conda create -n recast python==3.7.10

conda activate recast
conda install -c conda-forge cmake cppzmq eigen boost fftw libastra

git clone --recursive <repo>
mkdir build && cd build
cmake ../ -DCMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"} -DCMAKE_BUILD_TYPE=RELEASE
```

## Authors

RECAST3D is developed by the Computational Imaging group at CWI. Original author:

- Jan-Willem Buurlage (@jwbuurlage)

Contributions by:

- Holger Kohr (@kohr-h)
- Willem Jan Palenstijn (@wjp)
- Allard Hendriksen (@ahendriksen)
- Adriaan Graas (@adriaangraas)
- Daan Pelt (@dmpelt)
- Jun Zhu (@psi.ch)

## Contributing

We welcome contributions. Please submit pull requests against the develop
branch.

If you have any issues, questions, or remarks, then please open an issue on
GitHub.

## Publications using RECAST3D

| Article      |  Code  |
|------------------|--------|
| *Real-time reconstruction and visualisation ... at TOMCAT*. Sci.Rep. [DOI](https://doi.org/10.1038/s41598-019-54647-4) |  |
| *Real-time quasi-3D tomographic reconstruction*. MST. [DOI](https://doi.org/10.1088/1361-6501/aab754)  | [<img src="https://github.com/favicon.ico" width="24">](https://github.com/cicwi/RECAST3D) |

## Please cite us

If you have used RECAST3D for a scientific publication, we would appreciate
citations to the following paper:

[Real-time quasi-3D tomographic reconstruction. JW Buurlage, H Kohr, WJ
Palenstijn, KJ Batenburg. Measurement Science and Technology
(2018)](https://doi.org/10.1088/1361-6501/aab754)

## License

This project is licensed under the GPL. See `LICENSE.md` for details.

[TomoPackets]: https://www.github.com/cicwi/TomoPackets
[SliceRecon]: https://www.github.com/cicwi/SliceRecon
[installation documentation]: https://cicwi.github.io/RECAST3D/installation_instructions/
