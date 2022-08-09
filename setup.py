# odslatex-qt: a Qt5 interface to odslatex.
#
# Copyright (c) 2022, Javier Garcia.
#
# This file is part of odslatex-qt.
#
# odslatex-qt is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# odslatex-qt is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with
# odslatex-qt. If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
        name = 'odslatex-qt',
        version = '0.1',
        author = 'Javier Garcia', 
        long_description = 'No description for now',
        packages = find_packages(),
        entry_points = {
            'gui_scripts' : [
                'odslatex_qt = odslatex_qt.main:main'
                ]
            },
        package_data = {'': ['odslatex_qt/main.ui']},
        include_package_data=True,
        install_requires = [
            'PyQt5',
            'odslatex>=0.3.1',
            'importlib_resources'
            ]
        )
