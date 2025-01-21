py -3.10 -m build --wheel
rmdir build /s /q
rmdir scisuit.egg-info /s /q


py -3.11 -m build --wheel
rmdir build /s /q
rmdir scisuit.egg-info /s /q

py -3.12 -m build --wheel
rmdir build /s /q
rmdir scisuit.egg-info /s /q

py -3.13 -m build --wheel
rmdir build /s /q
rmdir scisuit.egg-info /s /q