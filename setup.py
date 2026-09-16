from setuptools import find_packages, setup

package_name = 'magic_button'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ltcc',
    maintainer_email='ltcc426@gmail.com',
    description='Custom WASD keyboard controller with a 360-degree magic action for ROS2 turtlesim.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'magic_button = magic_button.magic_button:main',
        ],
    },
)
