
def check_for_svn():
    """
    Checks if the `svn` program is installed
    and if it is available in the PATH.
    """
    import distutils
    import os
    if os.name == "nt":
        executable = "svn.exe"
    else:
        executable = "svn"

    if distutils.spawn.find_executable(executable) is None:
        if os.name == "nt":
            message = (
                "The SVN executable seems to missing from your path in this machine. "
                "Contact IT and ask them to reinstall TortoiseSVN and ensure that "
                "the 'Add SVN executables to PATH` option is selected.")
        else:
            message = (
                "The svn executable doesn't seem to be available in the path. "
                "Reconfigure the PATH variable so that it is reachable, "
                "or check if it is installed in the first place.")
        raise EnvironmentError(message)
