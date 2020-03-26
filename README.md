# vimbaPy

This is the development branch for code that may make it into a future release. Note that there is currently only support for `pymba`, support for `VimbaPython` will be added in due course. Documentation can found with their respective methods in the source code. 

### Installation

To install the package, simply clone this branch to a suitable directory

``` shell
# Clone to desktop (for e.g.)
cd ~/Desktop

git clone -b dev --single-branch https://github.com/EmbryoPhenomics/vimbaPy.git

```
and then install using pip:

``` shell

cd vimbaPy

# Uninstall any existing version of vimbaPy
pip uninstall vimbaPy 

# and install
pip install .

```

If you are on linux you may need to use root privileges:

``` shell

sudo pip install .

```

If you'd like to install `vimbaPy` for a specific python version, use the following:

``` shell
# For python 3.8
sudo -H python3.8 -m pip install .

```
#### Known installation errors

Doing a normal pip installation may not work and so you may need to install `vimbaPy` for the version of python you intend to use (please see above). 

#### Installing pymba 

You can install `pymba` using pip:

``` shell

pip install pymba

```

If you are on linux, you may need to use root privileges:

``` shell 

sudo pip install pymba

```

For installing vimba please see the installation guides for your OS [here](https://www.alliedvision.com/en/products/software.html#c6444).
