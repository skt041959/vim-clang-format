import vim
import difflib
from subprocess import run

def format_and_replace(cmd):
    curbuf = vim.current.buffer
    buffer_content = curbuf[:]
    proc = run(cmd, input='\n'.join(curbuf[:]).encode('utf8'), capture_output=True)
    if proc.returncode != 0:
        vim.err_write(proc.stderr.decode('utf8') + '\n')
        return

    buffer_formatted = proc.stdout.decode('utf8').splitlines(keepends=False)
    groups = list(
        filter(
            lambda x: x[0] != 'equal',
            difflib.SequenceMatcher(None, buffer_content,
                                    buffer_formatted).get_opcodes()))
    vim.out_write(str(cmd) + '\n')
    vim.out_write(str(groups) + '\n')
    if not groups:
        return
    tag, i1, _, j1, _ = groups[0]
    tag, _, i2, _, j2 = groups[-1]
    curbuf[i1:i2] = buffer_formatted[j1:j2]
