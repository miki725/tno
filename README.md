# Django Initium

A Django project start template.

    $ django-admin.py startproject \
          --template=http://bit.ly/django-initium \
          --extension=py,sh \
          project_name

***Note:*** Please make sure that you provide all extensions above
 as they are required in order to render some helper tools.

This project does not include any of the standard css/js libraries one
would need to use this template (e.g. bootstrap) due to their
rapid release cycles (it would clog the repo constantly updating them).
To compensate for that, it includes a bunch of initialization scripts
which will download the latest versions of the necessary libraries.
They are located at `init` directory:

    $ cd init && ./init-static.sh

Also since there are git and mercurial people, this template includes
ignore files for both vcs. So it might be a good idea to delete
the innapropriate ignore list file:

    $ # since we are at github
    $ rm .hgignore   

Credits
-------

* Miroslav Shubernetskiy <miroslav@miki725.com>

License
-------

::

    The MIT License (MIT)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
