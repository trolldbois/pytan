#$PYTHON='python'
$PYTHON='python3'

$parent_dir=(split-path -parent $my_dir)
$pytan_ext_dir="$parent_dir\pytan\ext"
$pytan_winext_dir="$parent_dir\pytan\winext"

$env:PYTHONPATH="$env:PYTHONPATH:$parent_dir;$pytan_winext_dir"
$env:PYTHON_VERSION=(&$PYTHON --version)
