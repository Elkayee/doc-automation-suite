"""Console companion for the portable Windows application."""

import argparse
import sys

from src.cli import cli


def main():
    for stream in (sys.stdout, sys.stderr):
        if stream is not None:
            stream.reconfigure(encoding='utf-8')
    if sys.argv[1:2] == ['serve']:
        import uvicorn

        from src.api import app

        parser = argparse.ArgumentParser(description='Start the local document API.')
        parser.add_argument('serve')
        parser.add_argument('--port', type=int, default=8000)
        args = parser.parse_args()
        uvicorn.run(app, host='127.0.0.1', port=args.port)
    else:
        cli()


if __name__ == '__main__':
    main()
