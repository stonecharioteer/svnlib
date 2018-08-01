commit 0b08f42b10c6cbccd3f143aef6b6b386c08c03f8
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Wed Aug 1 11:27:56 2018 +0530

    FEATURE. Added get_info function, and added relevant tests.

commit 12cc5406d3a2f621f958e5682bafa174e669249b
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Wed Aug 1 11:27:06 2018 +0530

    Added logic to skip empty rows in the errors list.

commit c1e5089dfa630d6e60e23693351ead65190741b3
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 14:46:56 2018 +0530

    Bumped version to 0.1.2a

commit 7157563f5f0407dd7b1121c647048fa80d9e17a1
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 14:45:48 2018 +0530

    FEATURE. Implemented the move feature.

commit 60d5d44619697110f4369879ac8dc9b5a1a51c2a
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 11:26:23 2018 +0530

    Changed the test template to workorder_FEA.

commit be8197603f75d291dfd0d3e39ca5539649ca0aa7
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 11:22:34 2018 +0530

    Added failsafes for when the user doesn't have access to the repository in which the templates reside. This raises the PermissionsError.

commit 9a4a283290c2f427ae614b24fddb1471f63d1803
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 09:38:46 2018 +0530

    Added test for behaviour of the class attributes.

commit 593be42295f825ae42d273871134b0881d8682ab
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 09:24:22 2018 +0530

    Added an additional exception for folder creation validation. Both the create_folder and clone_template_folders have a new argument, validate, that defaults to False. If True, it checks if the folder has been created and raises the SVNFolderCreationException if it fails.

commit 7c0b4fe68781906817c1fbbe77ea9776f61a7048
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Tue Jul 31 09:23:25 2018 +0530

    Cleaned up the import statement.

commit 9b6938cd74ddc8f885a4cf13a4b16362bebfe20f
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 17:34:24 2018 +0530

    Changed version to 0.1.1a

commit 47ae39b37c4e19243415776effa99440d19145ad
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 17:18:05 2018 +0530

    Changed version to 0.1alpha.

commit dc476e01e18cb39dd822bbc81fbdf2794f424c1f
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 17:14:50 2018 +0530

    All tests work now.

commit 3e78c2500485b0a6d64565b3e68fbed02edc8398
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 17:14:28 2018 +0530

    Added tmp folder.

commit 52b78909117898167a9cb99d0f804451c1467288
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 15:25:48 2018 +0530

    Working on an efficient error parsing methodology.

commit 03a2f9ecab2aae9365b4a1eb4b5bbc5e73c81bec
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 15:25:27 2018 +0530

    Added tests.

commit 702029533279dd48df3775e748331fac95cf63ca
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 14:31:00 2018 +0530

    Fixed parenthesis placement error.

commit 958ac1559f437faa129c92c1223bec491e6055c7
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 14:24:45 2018 +0530

    Added missing parenthesis.

commit 56ff19cb1f1891266e122127666974f2d80ab22e
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 14:24:15 2018 +0530

    Added additional metadata to the setup file.

commit ec86af7fb8b5e605b46c1d5b4bb88c2221bba1dd
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 13:54:47 2018 +0530

    Added __name__

commit aadbcc96b7188488c1ce21659daca8ec83d18b21
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 13:53:38 2018 +0530

    Added readme.

commit 71831cf8e38b3c8d37f4facb63af2bd9e247887e
Author: Vinay Keerthi <Vinay.Keerthi@gkndriveline.com>
Date:   Mon Jul 30 13:53:04 2018 +0530

    Added readme.

commit 285044d14058297143109aebd7eca551c1a87634
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:46:57 2018 +0530

    Added makefiles.

commit caf153db5fd54e9aad824d87e349080fe5fee761
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:46:45 2018 +0530

    Added requirements.

commit 95d2b8c6a29d50cc33dd122c45b6a28049b19e07
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:46:31 2018 +0530

    Added setup file.

commit 4661ff584cec2c8bb31c05806346d24b09a66ff2
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:46:10 2018 +0530

    Refactored the library so that it'll use setuptools, and have detailed tests.

commit da766a8b7f13a1eb702fef6f3ba4afebfae504fc
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:45:46 2018 +0530

    Added test placeholders.

commit d324108f583e820b5bad86413307d6b069126ecb
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:45:12 2018 +0530

    Added documentation placeholders.

commit 4af247a3b59aec873e97db5e9d7d0d164519d9b1
Author: Vinay Keerthi <ktvkvinaykeerthi@gmail.com>
Date:   Mon Jul 30 13:37:16 2018 +0530

    Added gitignore.
