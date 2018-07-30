from .exceptions import SVNException

class SVNErrorParser:
    """Class to manage the errors from svn.
    """
    def __init__(self, err_list):
        """Intialization

        Arguments:
            err_list {list} -- Second output from `subprocess.Popen().communicate()`, the errors.
        """
        if isinstance(err_list, bytes):
            err_list = err_list.decode("ascii").strip()
            if err_list == "":
                err_list = []
            else:
                err_list = err_list.split("\r\n")
        
        self.parse_errors(err_list)

    def __repr__(self):
        """Representation method.

        Returns:
            str -- Representation of the instance, to be used only
                when no information about the instance is required.
        """

        return "<SVNErrorParser Instance>"

    def __str__(self):
        """String conversion method.

        Returns:
            str: String representation of the instance. To be used when one wishes
                to know about the errors in an easy-to-read way.
        """
        return ("SVNErrorParser. hostname_is_valid: {hostname_is_valid}; "
            "username_is_valid: {username_is_valid}; password_is_valid: {password_is_valid}, "
            "repo_exists: {repo_exists}; user_has_auth: {user_has_auth}.").format(**self.response())

    def response(self):
        """Response method.

        Returns:
            dict: A dictionary of the status of various errors that are possible.
        """
        return {
            "hostname_is_valid": self.hostname_is_valid,
            "username_is_valid": self.username_is_valid,
            "password_is_valid": self.password_is_valid,
            "repo_exists": self.repo_exists,
            "user_has_auth": self.user_has_auth
        }

    def parse_errors(self, err):
        """Method to parse the errors returned by subprocess.Popen().communicate().

        Arguments:
            err {list} -- list containing the output of the svn command.

        Raises:
            Exception -- When the error is neither a list or a string or None.
            Exception -- [description]
            Exception -- [description]
            Exception -- [description]
            Exception -- [description]
        """

        self.hostname_is_valid = None
        self.username_is_valid = None
        self.password_is_valid = None
        self.repo_exists = None
        self.user_has_auth = None
        self.item_exists = None
        if isinstance(err, list):
            if len(err) == 0:
                self.hostname_is_valid = True
                self.username_is_valid = True
                self.password_is_valid = True
                self.repo_exists = True
                self.user_has_auth = True
                self.item_exists = True
            else:
                for error in err:
                    if "unable to connect to a repository" in error.lower():
                        self.repo_exists = False
                    elif "unknown hostname" in error.lower():
                        self.hostname_is_valid = False
                    elif "no repository found" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists = False
                    elif "username not found" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists=True
                        self.username_is_valid = False
                    elif "password incorrect" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists = True
                        self.username_is_valid = True
                        self.password_is_valid = False
                    elif "authorization failed" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists = True
                        self.username_is_valid = True
                        self.password_is_valid = True
                        self.user_has_auth = False
                    elif "non-existent in revision" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists = True
                        self.user_has_auth = True
                        self.username_is_valid = True
                        self.password_is_valid = True
                        self.item_exists = False
                    elif "some targets don't exist" in error.lower():
                        self.hostname_is_valid = True
                        self.repo_exists = True
                        self.user_has_auth = True
                        self.username_is_valid = True
                        self.password_is_valid = True
                        self.item_exists = False
                    else:
                        raise SVNException(error)
        else:
            raise SVNException(str(err))
