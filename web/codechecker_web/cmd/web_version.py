# -------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -------------------------------------------------------------------------
"""
Defines a subcommand for CodeChecker which prints version information.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse
import json

from codechecker_common import logger
from codechecker_common import output_formatters

from codechecker_web.shared import webserver_context, version


def get_argparser_ctor_args():
    """
    This method returns a dict containing the kwargs for constructing an
    argparse.ArgumentParser (either directly or as a subparser).
    """

    return {
        'prog': 'CodeChecker webserver version',
        'formatter_class': argparse.ArgumentDefaultsHelpFormatter,

        # Description is shown when the command's help is queried directly
        'description': "Print the version of CodeChecker server package that "
                       "is being used.",

        # Help is shown when the "parent" CodeChecker command lists the
        # individual subcommands.
        'help': "Print the version of CodeChecker server package that is "
                "being used."
    }


def add_arguments_to_parser(parser):
    """
    Add the subcommand's arguments to the given argparse.ArgumentParser.
    """

    parser.add_argument('-o', '--output',
                        dest='output_format',
                        required=False,
                        default='table',
                        choices=output_formatters.USER_FORMATS,
                        help="The format to use when printing the version.")

    logger.add_verbose_arguments(parser)
    parser.set_defaults(func=main)


def print_version(output_format=None):
    """
    Print web server version information in the given format.
    """
    context = webserver_context.get_context()

    server_versions = ['{0}.{1}'.format(major, minor) for
                       major, minor in version.SUPPORTED_VERSIONS.items()]

    if output_format != 'json':
        server_versions = ', '.join(server_versions)

    rows = [
        ("Base package version", context.version),
        ("Package build date", context.package_build_date),
        ("Git commit ID (hash)", context.package_git_hash),
        ("Git tag information", context.package_git_tag),
        ("Configuration schema", str(context.product_db_version_info)),
        ("Database schema", str(context.run_db_version_info)),
        ("Server supported API (Thrift)", server_versions),
        ("Client API (Thrift)", version.CLIENT_API)
    ]

    if output_format != "json":
        print(output_formatters.twodim_to_str(output_format,
                                              ["Kind", "Version"],
                                              rows))
    elif output_format == "json":
        # Use a special JSON format here, instead of
        # [ {"kind": "something", "version": "0.0.0"}, {"kind": "foo", ... } ]
        # do
        # { "something": "0.0.0", "foo": ... }
        print(json.dumps(dict(rows)))


def main(args):
    """
    Get and print the version information from the version config
    file and Thrift API definition.
    """
    logger.setup_logger(args.verbose if 'verbose' in args else None)

    print_version(args.output_format)
