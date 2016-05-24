$PYTHON='python'
#$PYTHON='python3'

$parent_dir=(split-path -parent $my_dir)
$pytan_ext_dir="$parent_dir\pytan\ext"

$env:PYTHONPATH="$env:PYTHONPATH:$parent_dir"
$env:PYTHON_VERSION=(&$PYTHON --version)
