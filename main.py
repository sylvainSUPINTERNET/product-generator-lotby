
# https://betterprogramming.pub/designing-beautiful-command-line-applications-with-python-72bd2f972ea

from CredentialManager import CredentialManager

import click

cm = None


@click.group()
def app():
    """Product generator for stripe, made by sylvain for lotby"""






@app.command()
@click.option("--count", default=1, help="How much love you want")
@click.argument("name")
def spread(name, count):
    """Spread the love."""
    
    print(cm)
    cm.print_credentials()
    
    for i in range(count):
        print(f"{name} loves you ❤️")


@app.command(name="print")
@click.argument("filepath", metavar="FILE", type=click.Path(exists=True))
@click.option("--show-meta", default=False, is_flag=True)
def print_(filepath, show_meta):
    """Print the file."""
    if show_meta:
        print(f"File path: {filepath}")
        print("-" * 80)
    with open(filepath, "r") as f:
        print(f.read())


if __name__ == "__main__":

    stripe_pk = click.prompt('Stripe public key', type=str)
    stripe_sk = click.prompt('Stripe secret key', type=str)
    
    cm = CredentialManager(stripe_pk, stripe_sk)
    
    app()