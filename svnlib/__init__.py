"""
===============
svnlib library
===============

A customized subversion API built in Python.

Coverage: Features are only coded on demand into this library. It is different
from the pysvn library in that it can operate on remote repositories without 
checking them out.

"""
__name__ = "svnlib"
from .internals import check_for_svn
try:
    check_for_svn()
except:
    raise
else:
    del check_for_svn

from .svn_error_parser import SVNErrorParser
from .svnlib import (
            get_hostname,
            get_info,
            list_folder,
            check_credentials,
            check_authorization,
            checkout,
            export,
            commit,
            item_exists,
            create_folder,
            clone_template_folders,
            delete_folder,
            move_folder,
            import_item,
            create_repository,
            get_templates_folder # meta.
            )
