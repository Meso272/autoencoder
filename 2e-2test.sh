#! /bin/bash
source ~/.bashrc
conda activate tf
cd lossycompression/autoencoder
python do_aramco.py aramco 0 2e-2res/aramco 2
python do_Hurricane.py U 0 2e-2res/U 2
python do_Hurricane.py QVAPOR 0 2e-2res/QVAPOR 2
python do_Nyx.py baryon_density 0 2e-2res/bdlog 2
python do_Nyx.py temperature 0 2e-2res/tlog 2
python do_Nyx.py dark_matter_density 0 2e-2res/dmdlog 2