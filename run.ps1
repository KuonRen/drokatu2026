# VSCode loads this file automatically when opening a project terminal.
# Outside VSCode, load it with: . .\run.ps1
function run {
    if ($args.Count -eq 0) {
        throw 'Usage: run <Python file> [arguments...]'
    }

    & py -m uv run --locked --project $PSScriptRoot python @args
}
