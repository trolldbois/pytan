$PYTHON='python'
$PYTAN_PATH='C:\GitHub\pytan'

$env:PYTHONPATH="$env:PYTHONPATH:$PYTAN_PATH\lib"
$env:PYTHON_VERSION=(&$PYTHON --version)
