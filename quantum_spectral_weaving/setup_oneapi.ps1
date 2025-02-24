# fr fr setup quantum environment w oneapi EXPEDITIOUSLY
$envName = "quantum_weaving"
$oneapiPath = "C:\Program Files (x86)\Intel\oneAPI"
$setvarsPath = "$oneapiPath\setvars.bat"

# yeet existing env fr fr
conda env remove -n $envName

# create fresh environment NO CAP
conda create -n $envName python=3.9 -y

# activate environment expeditiously
conda activate $envName

# initialize oneapi environment variables BUSSIN
cmd /c "call `"$setvarsPath`" intel64 vs2022 && set > %temp%\vars.txt"
Get-Content "$env:TEMP\vars.txt" | foreach-object {
    if ($_ -match '=') {
        $v = $_.split('='); [System.Environment]::SetEnvironmentVariable($v[0], $v[1], "Process")
    }
}

# install them oneapi deps fr fr
conda install numpy scipy pytest -y
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
python -m pip install intel-extension-for-pytorch
python -m pip install oneccl_bind_pt --no-deps
python -m pip install git+https://github.com/NeoVertex1/ComplexTensor.git

# set them environment variables for MAXIMUM OPTIMIZATION
$env:DPCPP_CPU_NUM_CORES = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
$env:ONEDNN_MAX_CPU_ISA = "AVX512_CORE_AMX"
$env:CCL_WORKER_COUNT = 4
$env:CCL_LOG_LEVEL = "ERROR"
$env:PYTHONPATH = "$oneapiPath\pytorch\latest\lib;$env:PYTHONPATH"

# install our package in develop mode NO CAP
pip install -e .

# verify installation EXPEDITIOUSLY
python -c "import torch; print(f'pytorch using {torch.backends.mkldnn.is_available()=}'); from quantum_spectral_weaving import *; print('quantum environment BUSSIN w oneapi fr fr')"

# run them tests
pytest tests/ -v
