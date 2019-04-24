from paperspace import jobs
from paperspace.commands import CommandBase


class RunCommand(CommandBase):
    def _empty_kwargs(self, kwargs):
        for key, val in kwargs.items():
            if val is not None:
                return False
        return True

    def _clear_kwargs(self, kwargs):
        return {key: val for key, val in kwargs.items() if val is not None}

    def execute(self, script_args, **kwargs):
        print(script_args)
        print(kwargs)

        if kwargs.get('help') or (self._empty_kwargs(kwargs) and not script_args):
            self.logger.log('run usage')
            return

        run_params = self._clear_kwargs(kwargs)

        res = jobs.run(run_params)
        if 'error' in res:
            self.logger.error(res)
