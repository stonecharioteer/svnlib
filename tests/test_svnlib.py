import os
import tempfile
import shutil
import sys
import uuid
import warnings
import shutil
TEST_USER = TEST_PASSWORD = "svnuser"
TEST_TEMPLATE = "workorder_FEA"
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

    err = svnlib.check_credentials("{}{}".format(TEST_USER, uuid.uuid4()), TEST_PASSWORD)
    assert err.hostname_is_valid == True
    assert err.repo_exists == True
    assert err.username_is_valid == False
    assert err.password_is_valid is None

    err = svnlib.check_credentials(TEST_USER, "{}{}".format(TEST_PASSWORD, uuid.uuid4()))
    assert err.hostname_is_valid == True
    assert err.repo_exists == True
    assert err.username_is_valid == True
    assert err.password_is_valid == False

def test_auth():
    err = svnlib.check_authorization(
        "svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert err.repo_exists == True
    assert err.user_has_auth == True
    err = svnlib.check_authorization(
        "svn://{}/XT4210/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert err.repo_exists == True
    assert err.user_has_auth == True

    assert err.user_has_auth == True
    # Assumption, the TEST_USER should not have 
    # access to the `jenkins` repository.
    err = svnlib.check_authorization(
        "svn://{}/jenkins/".format(SVN_SERVER), 
        TEST_USER, TEST_PASSWORD)
    assert err.repo_exists == True
    assert err.user_has_auth == False

def test_info():
    info, err = svnlib.get_info("svn://{}/xyz".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    expected_keys = [
        "URL","Relative URL", "Path",
        "Repository Root","Repository UUID",
        "Revision","Node Kind","Last Changed Author",
        "Last Changed Rev","Last Changed Date"
        ]
    assert err.user_has_auth == True
    assert err.repo_exists == True
    assert err.item_exists == True

    for key in expected_keys:
        assert key in info.keys()
    for key in info.keys():
        assert key in expected_keys
    info, err = svnlib.get_info(
        "svn://{}/xyz/{}".format(SVN_SERVER, uuid.uuid4()), TEST_USER, TEST_PASSWORD)
    assert len(info.keys()) == 0
    assert err.item_exists == False
    assert err.repo_exists == True

def test_list():
    out, err = svnlib.list_folder("svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    assert isinstance(out, list) == True
    assert isinstance(err, svnlib.SVNErrorParser) == True

def test_behaviour():
    """This tests the attributes for expected behaviour
    under specific situations.
    This behaviour plays an important role in the usage of this
    module.
    """
    # Check if user has auth to a repository,
    # when querying for a folder that doesn't exist.
    test_url = "svn://{}/xyz/{}".format(SVN_SERVER, uuid.uuid4())
    err = svnlib.check_authorization(test_url, TEST_USER, TEST_PASSWORD)
    assert err.hostname_is_valid == True, "The hostname should be valid!"
    assert err.repo_exists == True, "The repo should exist."
    assert err.item_exists == False, "The subfolder in the repo should not exist."

    # Check hostname_is_valid

def test_checkout():
    temp_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    if os.path.exists(temp_dir):
        raise Exception("Cleanup your previous environment!")
    os.makedirs(temp_dir)
    checkout_dir = svnlib.checkout(
        "svn://{}/xyz".format(SVN_SERVER), temp_dir, TEST_USER, TEST_PASSWORD, depth="immediates")
    assert os.path.isdir(checkout_dir) == True
    assert os.path.isdir(os.path.join(checkout_dir,".svn")) == True
    items, err = svnlib.list_folder(
        "svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    for item in items:
        checkout_location = os.path.join(
            checkout_dir, os.path.basename(item))
        assert os.path.exists(checkout_location) == True
    # ensure it got nothing else.
    try:
        shutil.rmtree(temp_dir)
    except PermissionError:
        warnings.warn(
            "Unable to delete {}. Clean up your environment manually.".format(temp_dir))
    except:
        raise

def test_export():
    temp_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    os.makedirs(temp_dir)
    export_dir = svnlib.export("svn://{}/xyz".format(SVN_SERVER),
                            temp_dir, TEST_USER, TEST_PASSWORD, depth="immediates")
    assert os.path.isdir(export_dir) == True
    assert os.path.isdir(os.path.join(export_dir, ".svn")) == False
    items, err = svnlib.list_folder(
        "svn://{}/xyz/".format(SVN_SERVER), TEST_USER, TEST_PASSWORD)
    for item in items:
        export_location = os.path.join(
            export_dir, os.path.basename(item))
        assert os.path.exists(export_location) == True
    try:
        shutil.rmtree(temp_dir)
    except PermissionError:
        warnings.warn(
            "Unable to delete {}. Clean up your environment manually.".format(temp_dir))
    except:
        raise


def test_creation():
    test_folder = "test_{}".format(uuid.uuid4())
    test_url = "svn://{}/xyz/{}".format(SVN_SERVER, test_folder)
    assert svnlib.item_exists(test_url, TEST_USER, TEST_PASSWORD) == False

    out, err = svnlib.create_folder(test_url,
                                TEST_USER, TEST_PASSWORD,
                                commit_message="Creating folder for automated test of svnlib.")
    assert svnlib.item_exists(
        test_url, TEST_USER, TEST_PASSWORD) == True

    # test creation of template folders.
    template = TEST_TEMPLATE
    template_url = "{}/{}".format(svnlib.get_templates_folder(), template)
    assert svnlib.item_exists(
        template_url, TEST_USER, TEST_PASSWORD) == True

    template_folders, err = svnlib.list_folder(template_url,
                                        TEST_USER,
                                        TEST_PASSWORD,
                                        depth="infinity")
    assert err.user_has_auth == True # the template folder is in another repository.
    assert len(template_folders) > 0
    assert isinstance(template_folders[0], str) == True
    template_folders = [f for f in template_folders if os.path.splitext(f)[1] == ""]
    commit_message = "Cloning {} template folder for automated test of svnlib.".format(template)
    svnlib.clone_template_folders(test_url,
                                template,
                                TEST_USER,
                                TEST_PASSWORD,
                                commit_message=commit_message)

    for template_folder in template_folders:
        cloned_folder_url = "{}/{}".format(test_url, template_folder)
        assert svnlib.item_exists(
            cloned_folder_url, TEST_USER, TEST_PASSWORD) == True

    out, err = svnlib.delete_folder(test_url,
                                TEST_USER, TEST_PASSWORD,
                                commit_message="Deleting folder for automated test of svnlib.")
    assert svnlib.item_exists(
        test_url, TEST_USER, TEST_PASSWORD) == False

def test_move():
    test_folder = "test_{}".format(uuid.uuid4())
    test_url = "svn://{}/xyz/{}".format(SVN_SERVER, test_folder)
    assert svnlib.item_exists(
                        test_url, TEST_USER,
                        TEST_PASSWORD) == False
    out, err = svnlib.create_folder(test_url,
                                TEST_USER, TEST_PASSWORD,
                                commit_message="Creating folder for automated test of svnlib.")
    assert svnlib.item_exists(
        test_url, TEST_USER, TEST_PASSWORD) == True
    new_test_folder = "test_{}".format(uuid.uuid4())
    new_test_url = "svn://{}/xyz/{}".format(SVN_SERVER, new_test_folder)
    out, err = svnlib.move_folder(
        test_url, new_test_url, TEST_USER, TEST_PASSWORD, commit_message="moving folder for automated test of svnlib.")
    assert svnlib.item_exists(
        test_url, TEST_USER, TEST_PASSWORD) == False
    assert svnlib.item_exists(
        new_test_url, TEST_USER, TEST_PASSWORD) == True
    out, err = svnlib.delete_folder(new_test_url,
                        TEST_USER, TEST_PASSWORD,
                        commit_message="Deleting folder for automated test of svnlib.")
    assert svnlib.item_exists(
        new_test_url, TEST_USER, TEST_PASSWORD) == False

def test_import_folder():
    """
    Tests the import_folder functionality.
    
    """
    import tempfile
    import random
    import hashlib

    # Ready the temporary file.
    test_folder_location = os.path.join(
                                tempfile.gettempdir(),
                                str(uuid.uuid4()))
    os.makedirs(test_folder_location)
    test_file_path = os.path.join(
                            test_folder_location,
                            "{}.bin".format(uuid.uuid4()))
    # create a random binary file that's between 1 and 100 kb in size.
    file_size = 1024 * random.randint(1, 100)
    with open(test_file_path, "wb") as f:
        f.write(os.urandom(file_size))
    input_file_size = os.path.getsize(test_file_path)
    assert input_file_size == file_size
    with open(test_file_path, "rb") as f:
        input_file_hash = hashlib.sha256(f.read()).hexdigest()
    
    # import the folder into a repository.
    test_repository = "svn://{}/xyz".format(SVN_SERVER)
    err = svnlib.import_item(
                test_repository,
                test_folder_location,
                TEST_USER,
                TEST_PASSWORD,
                commit_message="Importing folder for automated test of svnlib.")

    test_url = "{}/{}".format(test_repository, 
                        os.path.basename(test_folder_location))
    folder_exists = svnlib.item_exists(
                                test_url, TEST_USER, 
                                TEST_PASSWORD)
    assert folder_exists == True

    # check if item exists.
    file_url = "{}/{}".format(test_url, os.path.basename(test_file_path))
    file_exists = svnlib.item_exists(file_url, TEST_USER, TEST_PASSWORD)

    assert file_exists == True

    # Check if the file was properly loaded.
    try:
        shutil.rmtree(test_folder_location)
    except PermissionError:
        warnings.warn("unable to delete the temp folder created for test.")
        export_location = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        test_folder_location = os.path.join(export_location, 
                                            os.path.basename(test_folder_location))
        test_file_path = os.path.join(test_folder_location,
                            os.path.basename(test_file_path))
    except:
        raise
    else:
        export_location = tempfile.gettempdir()

    svnlib.export(test_url, export_location, TEST_USER, TEST_PASSWORD)
    svnlib.delete_folder(test_url, 
                        TEST_USER, TEST_PASSWORD,
                        commit_message="Removing folder created for svnlib automated test.")
    assert os.path.exists(test_folder_location) == True
    assert os.path.isdir(test_folder_location) == True
    assert os.path.exists(test_file_path) == True
    assert os.path.isfile(test_file_path) == True
    assert os.path.getsize(test_file_path) == input_file_size
    with open(test_file_path, "rb") as f:
        new_sha256sum = hashlib.sha256(f.read()).hexdigest()
    assert new_sha256sum == input_file_hash

    try:
        shutil.rmtree(test_folder_location)
    except PermissionError:
        warnings.warn("unable to delete the temp folder created for test.")
