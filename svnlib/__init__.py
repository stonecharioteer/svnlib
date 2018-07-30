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
            get_hostname, list_folder,
            check_credentials, check_authorization,
            checkout, export,
            create_repository, commit,
            check_if_folder_exists,
            create_folder, clone_template_folders,
            delete_folder, get_templates_folder)
