Requirements
------------

-  `Docker version 17 or
   later <https://docs.docker.com/install/#support>`__

Setup interactive notebook environment
-----------------------------

We setup the development environment in a Docker container with the
following command.

-  ``make init``

This command gets the resources for training and testing, and then
prepares the Docker image for the experiments. After creating the Docker
image, you run the following command.

-  ``make create-container``

The above command creates a Docker container from the Docker image which
we create with ``make init``, and then login to the Docker container.
Now we made the development environment. For create and evaluate the
model, you run the following command.

Development with Docker container
---------------------------------

This section shows how we develop with the created Docker container.

Edit source code
~~~~~~~~~~~~~~~~

Most of the source codes of this project,
``RAD Pipeline`` are stored in the
``rad_pipeline`` directory. Generated Docker
container mounts the project directory to ``/work`` of the container and
therefore when you can edit the files in the host environment with your
favorite editor such as Vim, Emacs, Atom or PyCharm. The changes in host
environment are reflected in the Docker container environment.

Update dependencies
~~~~~~~~~~~~~~~~~~~

When we need to add libraries in ``Dockerfile`` or ``requirements.txt``
which are added to working environment in the Docker container, we need
to drop the current Docker container and image, and then create them
again with the latest setting. To remove the Docker the container and
image, run ``make clean-docker`` and then ``make init-docker`` command
to create the Docker container with the latest setting.

Login Docker container
~~~~~~~~~~~~~~~~~~~~~~

Only the first time you need to create a Docker container, from the
image created in ``make init`` command. ``make create-container``
creates and launch the rad_pipeline container. After
creating the container, you just need run ``make start-container``.

Logout from Docker container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you logout from shell in Docker container, please run ``exit`` in
the console.


Credits
=======

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`cookiecutter-docker-science <https://docker-science.github.io/>`__
project template.
