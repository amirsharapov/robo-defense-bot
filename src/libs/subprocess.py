import subprocess
from dataclasses import dataclass


@dataclass
class ExecuteCommnadResponse:
    cmd: str
    did_communicate: bool
    process: subprocess.Popen

    stdout: str = None
    stderr: str = None

    @property
    def returncode(self):
        return self.process.returncode


def execute_command(
        cmd: str,
        wait: bool = True,
        strip_output: bool = True,
        raise_error: bool = True
) -> ExecuteCommnadResponse:
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    if not wait:
        return ExecuteCommnadResponse(
            cmd=cmd,
            did_communicate=False,
            process=process
        )

    process.wait()

    stdout, stderr = process.communicate(timeout=5)

    if strip_output:
        if stdout:
            stdout = stdout.strip()
        if stderr:
            stderr = stderr.strip()

    if raise_error and (process.returncode != 0 or stderr):
        raise RuntimeError(f"Command '{cmd}' failed with error: {stderr}")

    return ExecuteCommnadResponse(
        cmd=cmd,
        did_communicate=True,
        process=process,
        stdout=stdout,
        stderr=stderr
    )
