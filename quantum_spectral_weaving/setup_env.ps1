# fr fr setup quantum environment expeditiously
$envName = "quantum_weaving"

# yeet any existing environment w same name NO CAP
conda env remove -n $envName

# create fresh environment BUSSIN
conda create -n $envName python=3.9 -y

# activate that environment expeditiously
conda activate $envName

# install them dependencies fr fr
conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge -y
conda install numpy scipy pytest -y
pip install git+https://github.com/NeoVertex1/ComplexTensor.git

# install our package in develop mode NO CAP
pip install -e .

# verify installation EXPEDITIOUSLY
python -c "from quantum_spectral_weaving import *; print('quantum environment BUSSIN fr fr')"

# run them tests
pytest tests/ -v