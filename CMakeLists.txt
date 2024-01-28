cmake_minimum_required(VERSION 3.27.2)
set(CMAKE_CXX_STANDARD 20)
project(scisuit_pybind311)

#wxWidgets directories
include_directories(C:/_libs/wxWidgets/include)
include_directories(C:/_libs/wxWidgets/lib/mswu>)

#Python (3.11) directory
include_directories(C:/Python/Python311/include)

# core, gui and plot
include_directories($ENV{VSPROJ}/sci_libs)

file(GLOB cppfiles
     "cpp/*.h"
     "cpp/*.cpp"
)

add_executable(${PROJECT_NAME} WIN32 ${cppfiles})

target_compile_definitions(${PROJECT_NAME} PRIVATE _WINDOWS _USRDLL _UNICODE __WXMSW__ wxUSE_NATIVE_DATAVIEWCTRL
wxUSE_MENUBAR WXUSINGDLL _CRT_SECURE_NO_WARNINGS _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)

target_link_directories(${PROJECT_NAME} PRIVATE C:/_libs/wxWidgets/lib)
target_link_libraries(${PROJECT_NAME} $<$<CONFIG:Release>:wxmsw32u wxexpat wxjpeg wxpng wxscintilla wxtiff wxzlib>)


