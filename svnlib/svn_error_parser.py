
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
                err_list = err_list.split("\n")
        
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
        if isinstance(err, list):
            if len(err) == 0:
                self.hostname_is_valid = True
                self.username_is_valid = True
                self.password_is_valid = True
                self.repo_exists = True
                self.user_has_auth = True
            else:
                if "unable to connect to a repository" in err[0].lower():
                    if len(err) > 1:
                        if "password incorrect" in err[1].lower():
                            self.username_is_valid = True
                            self.password_is_valid = False
                            self.repo_exists = True
                            self.hostname_is_valid = True
                        elif "username not found" in err[1].lower():
                            self.username_is_valid = False
                            self.repo_exists = True
                            self.hostname_is_valid = True
                        elif "no repository found" in err[1].lower():
                            self.repo_exists = False
                            self.hostname_is_valid = True
                            self.username_is_valid = True
                            self.password_is_valid = True
                        elif "unknown hostname" in err[1].lower():
                            self.hostname_is_valid = False
                            notify = True
                        else:
                            raise Exception(str(err))
                    else:
                        raise Exception(str(err))
                elif "authorization failed" in err[0].lower():
                    self.hostname_is_valid = True
                    self.username_is_valid = True
                    self.password_is_valid = True
                    self.repo_exists = True
                    self.user_has_auth = False
                elif "non-existent in revision" in err[0].lower():
                    self.hostname_is_valid = True
                    self.username_is_valid = True
                    self.password_is_valid = True
                    self.repo_exists = False
                    self.user_has_auth = None
                elif ("error resolving case of" in err[0].lower()) \
                    or ("error resolving case of" in err[1].lower()):
                    self.hostname_is_valid = None
                    self.username_is_valid = None
                    self.password_is_valid = None
                    self.repo_exists = None
                    self.user_has_auth = None
                else:
                    raise Exception(str(err))
        elif isinstance(err, str) or isinstance(err, bytes):
            if isinstance(err, bytes):
                err = err.decode("utf-8")
            if "error resolving case of" in err.lower():
                self.hostname_is_valid = None
                self.username_is_valid = None
                self.password_is_valid = None
                self.repo_exists = None
                self.user_has_auth = None
            elif err.strip() == "":
                self.hostname_is_valid = True
                self.username_is_valid = True
                self.password_is_valid = True
                self.repo_exists = True
                self.user_has_auth = True
            else:
                raise Exception(err)
        elif err is None:
            self.hostname_is_valid = True
            self.username_is_valid = True
            self.password_is_valid = True
            self.repo_exists = True
            self.user_has_auth = True
        else:
            raise Exception(str(err))
