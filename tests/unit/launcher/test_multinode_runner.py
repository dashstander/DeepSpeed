from copy import deepcopy
from deepspeed.launcher import multinode_runner as mnrunner
from deepspeed.launcher.runner import encode_world_info, parse_args
import os
import pytest


@pytest.fixture
def runner_info():
    hosts = {'worker-0': [0, 1, 2, 3], 'worker-1': [0, 1, 2, 3]}
    world_info = encode_world_info(hosts)
    env = deepcopy(os.environ)
    return env, hosts, world_info


def test_pdsh_runner(runner_info):
    env, resource_pool, world_info = runner_info
    args = parse_args('')
    runner = mnrunner.PDSHRunner(args, world_info)
    cmd, kill_cmd = runner.get_cmd(env, resource_pool)
    assert cmd[0] == 'pdsh'
    assert env['PDSH_RCMD_TYPE'] == 'ssh'


def test_openmpi_runner(runner_info):
    env, resource_pool, world_info = runner_info
    args = parse_args('')
    runner = mnrunner.OpenMPIRunner(args, world_info, resource_pool)
    cmd = runner.get_cmd(env, resource_pool)
    assert cmd[0] == 'mpirun'


def test_slurm_runner(runner_info):
    env, resource_pool, world_info = runner_info
    args = parse_args('')
    runner = mnrunner.SlurmRunner(args, world_info, resource_pool)
    cmd = runner.get_cmd(env, resource_pool)
    assert cmd[0] == 'srun'


def test_mvapich_runner(runner_info):
    env, resource_pool, world_info = runner_info
    args = parse_args('')
    runner = mnrunner.MVAPICHRunner(args, world_info, resource_pool)
    cmd = runner.get_cmd(env, resource_pool)
    assert cmd[0] == 'mpirun'