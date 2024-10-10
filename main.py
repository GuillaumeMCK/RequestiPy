import click

import app


@click.command()
def main():
    app.start()


if __name__ == "__main__":
    main()
