@echo off
setlocal

:: List of Python versions to build
set PY_VERSIONS = pybind310 pybind311 pybind312 pybind313


for %%V in (%PY_VERSIONS%) do (
    echo ===================================================
    echo Building for %%V (Release)
    echo ===================================================
    
    cmake -G "NMake Makefiles" -DVARPY=%%V -DCMAKE_BUILD_TYPE=Release ..
    
    cmake --build . --config Release
)

echo All builds completed!
pause