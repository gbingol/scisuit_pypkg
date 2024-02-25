cmake_minimum_required(VERSION 3.27.2)
set(CMAKE_CXX_STANDARD 20)

if(NOT WIN32)
	message(FATAL_ERROR "Works only under Win32")
endif()

#set(VARPY scisuit_pybind310)
set(VARPY scisuit_pybind311)
#set(VARPY scisuit_pybind312)

project(${VARPY})



if(${VARPY} STREQUAL "scisuit_pybind310")
	set(PYLIB "python310")
	set(PYHOME "C:/Python/Python3106/")

elseif(${VARPY} STREQUAL "scisuit_pybind311")
	set(PYLIB "python311")
	set(PYHOME "C:/Python/Python311/")

elseif(${VARPY} STREQUAL "scisuit_pybind312")
	set(PYLIB "python312")
	set(PYHOME "C:/Python/Python3121/")
endif()

#wxWidgets directories
include_directories(C:/_libs/wxWidgets/include)
include_directories(C:/_libs/wxWidgets/lib/mswu)

#Python directory
include_directories(${PYHOME}/include)

# core and plot
include_directories($ENV{VSPROJ}/sci_libs)

file(GLOB cppfiles
     "cpp/*.h"
     "cpp/*.cpp"
)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
add_library(${PROJECT_NAME} SHARED ${cppfiles})

target_compile_definitions(${PROJECT_NAME} PRIVATE 
		PYBINDLIBRARY_EXPORTS _WINDOWS _USRDLL _UNICODE __WXMSW__ wxUSE_NATIVE_DATAVIEWCTRL
		wxUSE_MENUBAR WXUSINGDLL _CRT_SECURE_NO_WARNINGS _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)

target_link_directories(${PROJECT_NAME} PRIVATE C:/_libs/wxWidgets/lib)
target_link_directories(${PROJECT_NAME} PRIVATE $ENV{VSPROJ}/sci_libs/libs)
target_link_directories(${PROJECT_NAME} PRIVATE ${PYHOME}/libs)


target_link_libraries(${PROJECT_NAME} 
	python3 ${PYLIB} 
	wxmsw32u scisuit_core scisuit_plotter)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy 
	$<TARGET_FILE:${PROJECT_NAME}> ${CMAKE_SOURCE_DIR}/scisuit/${PROJECT_NAME}.dll)