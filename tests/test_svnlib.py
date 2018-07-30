import os
import shutil
import sys

TEST_USER = TEST_PASSWORD = "svnuser"

SVN_SERVER="dllohsr222.driveline.gkn.com" 
os.environ["SVN_SERVER"] = SVN_SERVER
import svnlib

def test_class():
    err = svnlib.check_credentials(TEST_USER, TEST_PASSWORD)
    assert isinstance(err, svnlib.SVNErrorParser) == True
    assert hasattr(err, "hostname_is_valid") == True
    assert hasattr(err, "username_is_valid") == True
    assert hasattr(err, "password_is_valid") == True
    assert hasattr(err, "repo_exists") == True
    assert hasattr(err, "user_has_auth") == True
    assert hasattr(err, "item_exists") == True

def test_connection():
    err = svnlib.check_credentials(TEST_USER, TEST_PASSWORD)
    assert err.hostname_is_valid == True
    assert err.repo_exists == True
    assert err.username_is_valid == True
    assert err.password_is_valid == True

    err = svnlib.check_credentials(TEST_USER + "afsdf", TEST_PASSWORD)
    assert err.hostname_is_valid == True
    assert err.repo_exists == True
    assert err.username_is_valid == False
    assert err.password_is_valid is None

    err = svnlib.check_credentials(TEST_USER, TEST_PASSWORD + "afsdf")
    assert err.hostname_is_valid == True
    assert err.repo_exists == True
    assert err.username_is_valid == True
    assert err.password_is_valid == False

def test_auth():
    err = svnlib.check_authorization("svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert err.user_has_auth == True

    err = svnlib.check_authorization(
        "svn://{}/jenkins/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert err.user_has_auth == False

def test_list():
    out, err = svnlib.list_folder("svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert isinstance(out, list) == True
    assert isinstance(err, svnlib.SVNErrorParser) == True

def test_checkout():
    temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"tmp")
    if os.path.exists(temp_dir):
        raise Exception("Cleanup your previous environment!")
    os.makedirs(temp_dir)

    err = svnlib.checkout("svn://{}/xyz".format(SVN_SERVER), temp_dir, TEST_USER, TEST_PASSWORD, depth="immediates")

    checkout_dir = os.path.join(temp_dir, "xyz")
    assert os.path.isdir(checkout_dir) == True
    assert os.path.isdir(os.path.join(checkout_dir,".svn")) == True

    
    items, err = svnlib.list_folder(
        "svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    
    for item in items:
        checkout_location = os.path.join(
            checkout_dir, os.path.basename(item))
        assert os.path.exists(checkout_location) == True
    
    # shutil.rmtree(temp_dir)

