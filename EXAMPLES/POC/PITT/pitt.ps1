$my_script=(split-path -leaf $myinvocation.invocationname)
$my_dir=(split-path -parent $myinvocation.mycommand.definition)

. $my_dir/config.ps1 $args

$env:PYTHONINSPECT=$null
$WORKER_PATH="$my_dir\pitt.py"
$PYTHON_OPTIONS=''

& $PYTHON $PYTHON_OPTIONS $WORKER_PATH $args

$EXITCODE=$lastexitcode
