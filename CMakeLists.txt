cmake_minimum_required(VERSION 3.27.2)
set(CMAKE_CXX_STANDARD 20)

if(NOT WIN32)
	message(FATAL_ERROR "Works only under Win32")
endif()

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_SOURCE_DIR}/scisuit)

#set(VARPY pybind310)
set(VARPY pybind311)
#set(VARPY pybind312)

project(${VARPY})


if(${VARPY} STREQUAL "pybind310")
	set(PYLIB "python310")
	set(PYHOME "C:/Python/Python3106/")

elseif(${VARPY} STREQUAL "pybind311")
	set(PYLIB "python311")
	set(PYHOME "C:/Python/Python311/")

elseif(${VARPY} STREQUAL "pybind312")
	set(PYLIB "python312")
	set(PYHOME "C:/Python/Python312/")
endif()



include_directories(C:/_libs/boost/)

#Python directory
include_directories(${PYHOME}/include)

# core and plot
include_directories($ENV{USERPROFILE}/soft_proj/sci_libs)

file(GLOB cppfiles
     "cpp/*.h"
     "cpp/*.cpp")

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
add_library(${PROJECT_NAME} SHARED ${cppfiles})

target_compile_definitions(${PROJECT_NAME} PRIVATE 
		PYBINDLIBRARY_EXPORTS _WINDOWS _USRDLL _UNICODE __WXMSW__ 
		WXUSINGDLL wxUSE_MENUBAR wxUSE_NATIVE_DATAVIEWCTRL
		_CRT_SECURE_NO_WARNINGS _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)


include(C:/vcpkg/scripts/buildsystems/vcpkg.cmake)

find_package(wxWidgets REQUIRED core base)

include(${wxWidgets_USE_FILE})
target_include_directories(${PROJECT_NAME} PRIVATE ${wxWidgets_INCLUDE_DIRS})

#target_link_directories(${PROJECT_NAME} PRIVATE ${wxWidgets_LIBRARY_DIRS} )
target_link_directories(${PROJECT_NAME} PRIVATE $ENV{USERPROFILE}/soft_proj/sci_libs/libs)
target_link_directories(${PROJECT_NAME} PRIVATE ${PYHOME}/libs)

target_link_libraries(${PROJECT_NAME}  ${wxWidgets_LIBRARIES} python3 ${PYLIB} scisuit_core scisuit_plotter)
