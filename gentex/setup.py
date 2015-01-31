from os.path import join, dirname


def configuration(parent_package='', top_path=None,
                  package_name='comat'):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(package_name, parent_package, top_path)
    config.add_extension('libmakecomat_',
                         sources=join(dirname(__file__), 'makecomat.c'),
                         libraries=['m'])
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(configuration=configuration)
