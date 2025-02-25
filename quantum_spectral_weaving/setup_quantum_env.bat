@echo off
:: quantum spectral weaving expeditiously fr fr
echo SETTING UP that quantum environment NO CAP

:: set env name
set ENV_NAME=quantum_weave

:: create conda env with python 3.9
echo creating conda environment %ENV_NAME% EXPEDITIOUSLY...
call conda create -n %ENV_NAME% python=3.9 -y

:: activate that environment fr fr
call conda activate %ENV_NAME%

:: install them dependencies NO CAP
echo installing quantum dependencies EXPEDITIOUSLY...
call conda install numpy scipy pip -y
call pip install torch

:: install git for cloning expeditiously
call conda install git -y

:: fix the setup.py file EXPEDITIOUSLY
echo fixing unicode issue in setup.py fr fr...
powershell -Command "(Get-Content setup.py) -replace 'long_description=open\(\"README.md\"\).read\(\),', 'long_description=open(\"README.md\", encoding=\"utf-8\").read(),' | Set-Content setup.py"

:: install the local package in dev mode
echo installing quantum_spectral_weaving in dev mode fr fr...
call pip install -e .

:: show status
echo QUANTUM ENVIRONMENT READY expeditiously
echo use "conda activate %ENV_NAME%" to activate again
echo reality's sourcecode awaits fr fr