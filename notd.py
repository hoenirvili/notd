#!/usr/bin/env python3

import signal

import click

import core


@click.command()
@click.option(
    '-c', '--config', default='', help='Custom gpio json settings file')
@click.option(
    '-r',
    '--red',
    default=False,
    is_flag=True,
    help='Turn on the red led from the baord')
@click.option(
    '-g',
    '--green',
    default=True,
    is_flag=True,
    help='Turn on the green led from the board')
@click.option(
    '-d',
    '--debug',
    default=False,
    is_flag=True,
    help='Run the command line in debug mode')
@click.argument(
    'number',
    type=click.IntRange(0x0, core.Display.MAX_DISPLAY_VALUE),
    required=False)
@click.pass_context
def cli(ctx, config, red, green, debug, number):
    """
    Command line tool for interacting with the DIY home
    made PCB connected with the Raspberry Pi
    """
    if not number:
        command_help(cli)
        ctx.exit(0)

    click.echo('[*] Running display screen for number {}'.format(number))
    with core.Display(
            number, config_path=config, red=red, green=green,
            debug=debug) as display:
        signal.signal(signal.SIGINT, lambda signum, frame: display.turn_knob())
        display.open()  # run the display and stop when we receive a signal


def command_help(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))
