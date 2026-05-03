import unittest

import make


class MakeCliTests(unittest.TestCase):
    def test_parse_test_subcommand(self):
        args = make.parse_args(['test'])
        self.assertEqual(args.command, 'test')

    def test_parse_build_subcommand(self):
        args = make.parse_args(['build', '--workspace', 'workspaces/3'])
        self.assertEqual(args.command, 'build')
        self.assertEqual(args.workspace, 'workspaces/3')


if __name__ == '__main__':
    unittest.main()
