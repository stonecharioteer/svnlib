# -*- coding: utf-8 -*-
import sys
import subprocess
import os

from .svn_error_parser import SVNErrorParser
from . import exceptions

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
    _, query_errors = list_folder(url, username, password)
    return query_errors

def get_info(url, username, password):
    """Returns the svn info for a repository."""
    args = [
            "svn", "info", url,
            "--username", username,
            "--password", password,
            "--no-auth-cache", "--non-interactive"
            ]
    process = subprocess.Popen(
                        args,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("latin-1")
    out = out.split("\r\n" if "\r\n" in out else "\n")
    err = SVNErrorParser(err)
    info_dict = {}
    if err.item_exists:
        for line in out:
            if line.strip() != "":
                key = line[:line.find(":")].strip()
                value = line[line.find(":")+1:].strip()
                info_dict[key] = value
    return info_dict, err

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
    out = out.decode("utf-8")
    out = out.split("\r\n" if "\r\n" in out else "\n")
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
    out, err = process.communicate()
    os.chdir(start_dir)
    return os.path.join(folder, os.path.basename(url))

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
    out, err = process.communicate()
    os.chdir(start_dir)
    return os.path.join(folder, os.path.basename(url))

def import_item(url,
        item_path, username, 
        password, commit_message=None, **kwargs):
    """
    helper function for `svn import`
    NOTE: This function fixes an odd caveat of `svn import`. Note that 
    this *could* be something I'm not aware of.
    Example: If you want to import a folder into a repository path, 
    `svn import` just imports the contents of that folder into 
    the location, and it doesn't bother creating said folder. 
    This is odd to me, at least, and seems very counter-intuitive.
    Hence the check to see if the given path is a folder and not a file.
    """
    if not os.path.exists(item_path):
        raise FileNotFoundError("{} is not a valid path".format(item_path))
    if commit_message is None:
        commit_message = "importing {}".format(item_path)
    if os.path.isdir(item_path):
        # if the folder doesn't exist on the repository,
        # make it and import the files into that location.
        folder_name = os.path.basename(item_path)
        url = "{}/{}".format(url, folder_name)
        if not item_exists(url, username, password):
            create_folder(
                        url, username, password,
                        commit_message=(
                            "Creating {} folder for "
                            "importing {} via svnlib."
                            ).format(folder_name, "folder_path"))
    args = ["svn", "import", "-m", commit_message,
            item_path, url, "--username",
            username, "--password",
            password, "--non-interactive", "--no-auth-cache"]

    for key in kwargs:
        args.extend(["--{}".format(key), str(kwargs[key])])
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    out, err = process.communicate()
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
        elif sys.version.startswith("2"):
            msg = (
                    "This feature is not meant for "
                    "Python 2.x. Use Python 3.4+.")
            raise EnvironmentError(msg)
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

def item_exists(link, user, password):
    """Checks if given link is reachable/exists.
    returns :bool:
    """
    args = ["svn", "info", "--username", user, "--password", password, link,
            "--depth", "empty", "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    errs = SVNErrorParser(err)
    return (errs.item_exists == True)

def create_folder(link, user, password, commit_message=None, parents=False, validate=False):
    """Creates an SVN folder."""
    if commit_message is None:
        commit_message = "Creating {}".format(link)
    if not parents:
        args = ["svn", "mkdir", "-m", commit_message,
                link,
                "--username", user, 
                "--password", password,
                "--non-interactive", "--no-auth-cache"]
    else:
        args = ["svn", "mkdir", "--parents", 
                "-m", commit_message,
                link, 
                "--username", user,
                "--password", password,
                "--non-interactive", "--no-auth-cache"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if validate:
        if not item_exists(link, user, password):
            raise exceptions.SVNFolderCreationError("Failed creating {}.".format(link))
    return out.decode("latin-1").strip(), SVNErrorParser(err)

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
    return out.decode("latin-1").strip(), SVNErrorParser(err)

def get_templates_folder():
    """Returns the link to the current FolderTemplates
    container in the XT4210 repository."""
    return "svn://{}/XT4210/apps/FolderTemplates/current".format(os.environ.get("SVN_SERVER", get_hostname()))

def clone_template_folders(link, template, user, password, commit_message=None, validate=False):
    """
    Creates the template folders as found in the corresponding template folder.
    TODO: Figure out what to do when there is a `loop` analysis run.
        Perhaps that needs to be client side.
    """
    required_template_folder = "{}/{}".format(get_templates_folder(), template)
    subfolders, err=list_folder(required_template_folder,
                            user, password, depth="infinity")
    if not err.user_has_auth:
        raise PermissionError(("User does not have access "
                    "to the templates folder {} "
                    "in the repository!").format(
                        required_template_folder))

    subfolders = ["{}/{}".format(link, folder)
                for folder in subfolders if (os.path.splitext(folder)[1] == "")]
    for folder in subfolders:
        if not item_exists(folder, user, password):
            create_folder(folder, user, password,
                        commit_message=commit_message, validate=validate)

def move_folder(link, new_link, user, password, commit_message=None, validate=False):
    """
    Moves a folder in an svn repository to another folder in the same repo.
    """
    if commit_message is None:
        commit_message = "Moving {} to {}".format(link, new_link)

    args = [
        "svn","move","-m", commit_message,
        link, new_link,
        "--username", user, "--password", password,
        "--no-auth-cache","--non-interactive"
    ]
    process = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode("latin-1").strip(), SVNErrorParser(err)

