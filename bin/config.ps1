if (!$my_dir){
    write-host "Need 'my_dir' defined to know where config.ps1 lives"
    exit(99)
}

$PYTHON='python'

$parent_dir=(split-path -parent $my_dir)
$pytan_ext_dir="$parent_dir\pytan\ext"

$env:PYTHONPATH="$env:PYTHONPATH:$parent_dir"
$env:PYTHON_VERSION=(&$PYTHON --version)
