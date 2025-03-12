cmake_minimum_required(VERSION 3.27.2)
set(CMAKE_CXX_STANDARD 20)

project(scisuit_package)

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_SOURCE_DIR}/scisuit)


include(C:/vcpkg/scripts/buildsystems/vcpkg.cmake)

set(USER_HOME_DIRECTORY $ENV{USERPROFILE})


#set(VARPY pybind310)
set(VARPY pybind311)
#set(VARPY pybind312)
#set(VARPY pybind313)

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

elseif(${VARPY} STREQUAL "pybind313")
	set(PYLIB "python313")
	set(PYHOME "C:/Python/Python313/")
endif()



#Python directory
include_directories(${PYHOME}/include)

# core and plot
include_directories(${USER_HOME_DIRECTORY}/soft_proj/scisuit/)

file(GLOB_RECURSE cppfiles
     "bindings/*.h"
     "bindings/*.cpp")


add_library(${PROJECT_NAME} SHARED ${cppfiles})

target_compile_definitions(${PROJECT_NAME} PRIVATE 
		PYBINDLIBRARY_EXPORTS _WINDOWS _USRDLL _UNICODE __WXMSW__ 
		WXUSINGDLL _CRT_SECURE_NO_WARNINGS _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)


find_package(wxWidgets REQUIRED core base)

target_include_directories(${PROJECT_NAME} PRIVATE ${wxWidgets_INCLUDE_DIRS})

target_link_directories(${PROJECT_NAME} PRIVATE 
						${USER_HOME_DIRECTORY}/soft_proj/scisuit/libs 
						${PYHOME}/libs)

target_link_libraries(${PROJECT_NAME}  
						${wxWidgets_LIBRARIES} 
						python3 
						${PYLIB} 
						scisuit_core 
						scisuit_plotter)