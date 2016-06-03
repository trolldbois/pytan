$my_script=(split-path -leaf $myinvocation.invocationname)
$my_dir=(split-path -parent $myinvocation.mycommand.definition)

if (!$my_dir){
    write-host "Need 'my_dir' defined to know where config.ps1 lives"
    exit(99)
}

. $my_dir/config.ps1 $args

$env:PYTHONINSPECT=$null
$WORKER_PATH="$my_dir\worker.py"
$PYTHON_OPTIONS='-B'

& $PYTHON $PYTHON_OPTIONS $WORKER_PATH "shell:$my_script" $args

$EXITCODE=$lastexitcode
