import sys

import mock
import pytest

from paperspace import main


class TestRun:
    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_with_no_parameters(self, mock_run):
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run']):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_not_called()
        # assert excinfo.value.code == 1

    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_script_name_parameters(self, mock_run):
        script_name = 'hello.py'
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run', script_name]):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_called_with({'script': script_name})
        assert excinfo.value.code == 0

    @pytest.mark.parametrize('param', ['--script', '--python', '--conda', '--ignoreFiles', '--apiKey', '--container',
                                       '--machineType', '--name', '--project', '--projectId', '--command',
                                       '--workspace', '--dataset', '--registryUsername', '--registryPassword',
                                       '--workspaceUsername', '--workspacePassword', '--cluster',
                                       '--clusterId', '--ports', '--isPreemptible', '--useDockerfile', '--buildOnly',
                                       '--registryTarget', '--registryTargetUsername', '--registryTargetPassword',
                                       '--relDockerfilePath', '--customMetrics', '--modelType', '--modelPath'])
    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_missing_parameter_value(self, mock_run, capsys, param):
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run'] + [param]):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        captured = capsys.readouterr()
        mock_run.assert_not_called()
        assert excinfo.value.code == 1
        assert 'error: missing argument for {}'.format(param) in captured.out

    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_all_parameters(self, mock_run):
        params = ['--script', 'hello.py', '--python', '2.7', '--conda', '2', '--ignoreFiles', '*', '--apiKey', '123',
                  '--container', 'containerName', '--machineType', 'G1', '--name', 'scriptName', '--project',
                  'projectName', '--projectId', 'projectHandle', '--command', 'cmd', '--workspace', 'workspaceUrl',
                  '--dataset', 'datasetUrl', '--registryUsername', 'username',
                  '--registryPassword', 'password', '--workspaceUsername', 'workUsername', '--workspacePassword',
                  'workPassword', '--cluster', 'cluster', '--clusterId', '1', '--ports', '5000', '--isPreemptible', 'False',
                  '--useDockerfile', 'False', '--buildOnly', 'False', '--registryTarget', 'registryTarget',
                  '--registryTargetUsername', 'rtUsername', '--registryTargetPassword', 'rtPassword',
                  '--relDockerfilePath', 'rDfP', '--customMetrics', 'metrics', '--modelType', 'model1', '--modelPath',
                  'modelPath1', '--init', '--req', '-m', '-c', '-', 'foo']
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run'] + params):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_called_with(
            {'script': 'hello.py', 'python': '2.7', 'conda': '2', 'ignoreFiles': '*', 'apiKey': '123',
             'container': 'containerName', 'machineType': 'G1', 'name': 'scriptName', 'project': 'projectName',
             'projectId': 'projectHandle', 'command': 'cmd', 'workspace': 'workspaceUrl', 'dataset': 'datasetUrl',
             'registryUsername': 'username', 'registryPassword': 'password', 'workspaceUsername': 'workUsername',
             'workspacePassword': 'workPassword--cluster', 'cluster': 'cluster', 'clusterId': '1', 'ports': '5000', 'isPreemptible': 'False',
             'useDockerfile': 'False', 'buildOnly': 'False', 'registryTarget': 'registryTarget',
             'registryTargetUsername': 'rtUsername', 'registryTargetPassword': 'rtPassword',
             'relDockerfilePath': 'rDfP', 'customMetrics': 'metrics', 'modelType': 'model1', 'modelPath': 'modelPath1',
             'init': True, 'req': True, 'run_module': True, 'script_args': ['-c', 'foo']})
        assert excinfo.value.code == 0

    @pytest.mark.parametrize('param', ['--no_logging', '--nologging', '--noLogging', '--json'])
    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_no_logging_parameters(self, mock_run, param):
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run', param]):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_called_with({'no_logging': True})
        assert excinfo.value.code == 0

    @pytest.mark.parametrize('param', ['dryrun', 'pipenv'])
    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_boolean_parameters(self, mock_run, param):
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run', '--%s' % param]):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_called_with({param: True})
        assert excinfo.value.code == 0

    @pytest.mark.parametrize('opts,run_params', [
        (['-', 'foo', 'bar'], {'script': 'foo', 'script_args': ['bar']}),
        (['-c', 'foo', 'bar'], {'run_command': True, 'script': 'foo', 'script_args': ['bar']}),
        (['-m', 'foo', 'bar'], {'run_module': True, 'script': 'foo', 'script_args': ['bar']}),
        (['-m', 'foo', 'bar', '-', 'baz'], {'run_module': True, 'script': 'foo', 'script_args': ['bar', 'baz']}),
        (['-m', 'foo', 'bar', '-', '-', 'baz'], {'run_module': True, 'script': 'foo', 'script_args': ['bar', 'baz']}),
        (['-m', 'foo', '-', 'bar', '-', 'baz'], {'run_module': True, 'script': 'foo', 'script_args': ['bar', 'baz']}),
        (['-', '-m', 'foo', 'bar', '-', 'baz'], {'script': '-m', 'script_args': ['foo', 'bar', 'baz']}),
        (['--script', 'foo', '-m', 'mod', '-', 'bar', 'baz'],
         {'script': 'foo', 'run_module': True, 'script_args': ['mod', 'bar', 'baz']}),
    ])
    @mock.patch("paperspace.commands.run.jobs.run")
    def test_run_job_with_script_args_parameters(self, mock_run, opts, run_params):
        with mock.patch.object(sys, 'argv', ['paperspace-python', 'run'] + opts):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
        mock_run.assert_called_with(run_params)
        assert excinfo.value.code == 0
