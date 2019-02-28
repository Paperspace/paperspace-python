import sys
import os
import argparse
import click

'''
This is our main cli group. Flags registered here do not need any subcommands to function. Keep these flags simple like
checking versions
'''
@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, default=False)
@click.pass_context
def cli(ctx, version):
    if version:
        click.echo("version new!")
        sys.exit(0)

'''
Login command registered off main cli group.
'''
@cli.command()
@click.option('--email', help="your paperspace email address")
@click.option('--password', help="your paperspace account password")
@click.option('--apiToken', help="your paperpace api token")
def login(email, password, apiToken):
    # perform login task
    click.echo("login {} {} {}".format(email, password, apiToken))

'''
Logout command registered off main cli group
'''
@cli.command()
def logout():
    # perform logout task
    click.echo("successefully logged out")

'''
Subcommand group "run" registered off main cli group. This allows for run subcommand to have it's own set of additional subcommands
'''
@cli.group()
@click.pass_context
def run(ctx):
    pass

# run python script
@run.command()
@click.pass_context
def script(ctx):
    click.echo("you're running a script {}", ctx.params)

# run python module
@run.command()
@click.pass_context
def script(ctx):
    click.echo("you're running a module! with params {}".format(ctx.params))

# run python command
@run.command()
@click.pass_context
def python_command(ctx):
    click.echo("you're running a python command! with params {}".format(ctx.params))

# run arbitrary command
@run.command()
@click.pass_context
def command(ctx):
    click.echo("you're running a command! with params {}".format(ctx.params))


if __name__ == "__main__":
    cli()
