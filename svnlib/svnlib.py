# -*- coding: utf-8 -*-
import sys
import subprocess
import os

from .svn_error_parser import SVNErrorParser

def get_hostname():
    """Returns the usual hostname at GKN DL."""
    # TODO: read this from the environment.
    import warnings
    warnings.warn(("Don't rely on the `get_hostname` function "
            "to retrieve the hostname. Instead, use the `SVN_SERVER` "
            "environment variable."))
    return "10.133.0.222"

def check_credentials(username, password):
    """Checks the svn credentials and returns an SVNErrorParser object."""
    _, query_errors = list_folder(
                "svn://{}/XT4210/".format(
                        os.environ.get("SVN_SERVER", get_hostname())),
                username, password)
    return query_errors

def check_authorization(url, username, password):
    """Checks if the given user has access to a repository,
    using the list function.

    Returns the query errors."""
    _, query_errors = list_folder(
        url, username, password)
    return query_errors

def list_folder(url, username, password, **kwargs):
    """Lists all folders inside an SVN repository URL.

    Arguments:
        url {str} -- valid svn repository url.
        username {str} -- username which needs to be used for the operation
        password {str} -- password

    Returns:
        str -- output of the `subversion.Popen().communicate()` command.
        SVNErrorParser -- errors, if any, from the process.
    """
    args = ["svn", "list", url,
            "--username",
            username, "--password",
            password, "--non-interactive",
            "--no-auth-cache"
            ]
    for key in kwargs:
        args.extend(["--{}".format(key), kwargs[key]])
    query_process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    out, err = query_process.communicate()

    out = out.decode("utf-8").split("\r\n")
    errors = SVNErrorParser(err)
    return out, errors

def checkout(url, folder, username, password, **kwargs):
    """Checkout an svn repository to a folder path using the user's credentials.

    Arguments:
        url {str} -- valid svn repository url.
        folder {str} -- path where an svn folder should be exported.
        username {str} -- username which needs to be used for the operation
        password {str} -- password

    Keyword Arguments:
        kwargs {[type]} -- [description] (default: {None})

    Returns:
        SVNErrorParser -- errors, if any, from the process.
    """
    start_dir = os.getcwd()
    os.chdir(folder)
    args = ["svn", "checkout", url, "--username",
            username, "--password",
            password, "--non-interactive", "--no-auth-cache"]
    # apply kwargs
    for key in kwargs:
        args.extend(["--{}".format(key), str(kwargs[key])])
    
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    try:
        out, err = process.communicate()
    except:
        os.chdir(start_dir)
        raise
    else:
        os.chdir(start_dir)
        return SVNErrorParser(err)

def export(url, folder, username, password, **kwargs):
    """Export an svn repository to a folder path using the user's credentials.

    Arguments:
        url {str} -- valid svn repository url.
        folder {str} -- path where an svn folder should be exported.
        username {str} -- username which needs to be used for the operation
        password {str} -- password

    Keyword Arguments:
        options {} -- Other options to pass to svn. UNIMPLEMENTED. (default: {None})

    Returns:
        SVNErrorParser -- errors, if any, from the process.
    """
    start_dir = os.getcwd()
    os.chdir(folder)
    args = ["svn", "export", url, "--username",
            username, "--password",
            password, "--non-interactive", "--no-auth-cache"]
    for key in kwargs:
        args.extend(["--{}".format(key),str(kwargs[key])])
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    try:
        out, err = process.communicate()
    except:
        os.chdir(start_dir)
        raise
    else:
        os.chdir(start_dir)
        return SVNErrorParser(err)

def get_cred():
    import warnings
    warnings.warn("Do not call this function, it is a security concern!")
    return {"username" : "svnuser", "password" : "svnuser"}

def create_repository(repository_name, 
                    username, password, 
                    svn_hostname, svn_host_user, 
                    svn_host_user_password):
    """Function to create a repository
    TODO: Find out how to store the SVN host name and passwords.

    COMMAND: cp -r /data/_repositories/_base_Repository_Template/ /data/_repositories/{0}; svnadmin setuuid /data/_repositories/{0}

    NOTE: Although this script creates the repositories, 
    note that access to the repositories is administered via the script in
    svn://dllohsr222/XT4210/apps/get_svn_users_groups/get_users_groups.py
    Only users in the Production Redmine session who are added as 
    members in a related project have access.
    """
    # first check if this exists.
    query = check_authorization(
                    "svn://{}/{}".format(
                        os.environ.get("SVN_SERVER", get_hostname()),
                        repository_name),
                    username, password)

    if query.repo_exists:
        # If the repository exists, raise a FileExistsError (Python3+) or a NameError.
        error_message = "{} already exists. Cannot overwrite the repository!".format(
            repository_name)
        try:
            raise FileExistsError(error_message)
        except:
            raise NameError(error_message)
    else:
        if os.name == "nt":
            raise OSError("This feature is unavailable on Windows based systems.")
        elif sys.startswith("2"):
            raise EnvironmentError("This feature is not meant for Python 2.x. Use Python 3.4+.")
        else:
            # If the repository doesn't exist, and if this is called from a Linux host,
            # then create the repository.
            from pexpect import pxssh
            server = pxssh.pxssh()
            server.login(svn_hostname, svn_host_user, svn_host_user_password)
            commands = (
                    "cp -r /data/_repositories/_base_Repository_Template/ "
                    "/data/_repositories/{0}; "
                    "svnadmin setuuid /data/_repositories/{0}").format(repository_name)
            server.sendline(commands)
            server.logout()

def commit(checkout_path, username, password, file_name, commit_message):
    """Commits changes made to a single file within a checked out repository."""
    start_dir = os.getcwd()
    os.chdir(checkout_path)
    args = ["svn", "commit", file_name, "-m", commit_message, "--username",
        username, "--password",
        password, "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    try:
        out, err = process.communicate()
    except:
        os.chdir(start_dir)
        raise
    else:
        os.chdir(start_dir)
        return SVNErrorParser(err)

def check_if_folder_exists(link, user, password):
    """Checks if an SVN folder exists.

    returns :bool:
    """
    args = ["svn", "list", "--username", user, "--password", password, link,
            "--depth", "empty", "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    errs = SVNErrorParser(err)
    return (errs.item_exists == True)

def create_folder(link, user, password, commit_message=None):
    """Creates an SVN folder."""
    if commit_message is None:
        commit_message = "Creating {}".format(link)
    args = ["svn", "mkdir", "-m", commit_message,
            "--username", user, "--password", password,
            link, "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("ascii").strip(), SVNErrorParser(err)

def delete_folder(link, user, password, commit_message=None):
    """Creates an SVN folder."""
    if commit_message is None:
        commit_message = "Deleting {}".format(link)
    args = ["svn", "rm", "-m", commit_message,
            "--username", user, "--password", password,
            link, "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("ascii").strip(), SVNErrorParser(err)

def get_templates_folder():
    """Returns the link to the current FolderTemplates container in the XT4210 repository."""
    return "svn://{}/XT4210/apps/FolderTemplates/current".format(os.environ.get("SVN_SERVER", get_hostname()))

def clone_template_folders(link, template, user, password, commit_message=None):
    """
    Creates the template folders as found in the corresponding template folder.
    TODO: Figure out what to do when there is a `loop` analysis run.
        Perhaps that needs to be client side.
    """
    required_template_folder = "{}/{}".format(get_templates_folder(), template)
    subfolders, err=list_folder(required_template_folder,
                            user, password, depth="infinity")
    
    subfolders = ["{}/{}".format(link, folder)
                for folder in subfolders if (os.path.splitext(folder)[1] == "")]
    for folder in subfolders:
        if not check_if_folder_exists(folder, user, password):
            create_folder(folder, user, password,
                        commit_message=commit_message)
