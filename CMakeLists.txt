cmake_minimum_required(VERSION 3.27.2)
set(CMAKE_CXX_STANDARD 20)

set(VARPY scisuit_pybind311)

project(${VARPY})

#wxWidgets directories
include_directories(C:/_libs/wxWidgets/include)
include_directories(C:/_libs/wxWidgets/lib/mswu)

#Python (3.11) directory
include_directories(C:/Python/Python311/include)

# core, gui and plot
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

if(${VARPY} STREQUAL "scisuit_pybind311")
	target_link_directories(${PROJECT_NAME} PRIVATE C:/Python/Python311/libs)

	target_link_libraries(${PROJECT_NAME} 
	python3 python311 
	wxmsw32u wxexpat wxjpeg wxpng wxscintilla wxtiff wxzlib 
	scisuit_core scisuit_gui scisuit_plotter)
endif()