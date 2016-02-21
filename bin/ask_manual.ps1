$my_script=(split-path -leaf $myinvocation.invocationname)
$my_dir=(split-path -parent $myinvocation.mycommand.definition)

. $my_dir/config.ps1 $args

#$env:PYTHONINSPECT="True"
$WORKER_PATH="$my_dir\worker.py"
$PYTHON_OPTIONS="-B"

python $PYTHON_OPTIONS $WORKER_PATH "shell:$my_script" $args

$EXITCODE=$lastexitcode
