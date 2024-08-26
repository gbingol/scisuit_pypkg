set(VARPY pybind310)
#set(VARPY pybind311)
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



#Python directory
include_directories(${PYHOME}/include)

# core and plot
include_directories(${CMAKE_SOURCE_DIR}/core_plot)

file(GLOB cppfiles
     "bindings/*.h"
     "bindings/*.cpp")


add_library(${PROJECT_NAME} SHARED ${cppfiles})

target_compile_definitions(${PROJECT_NAME} PRIVATE 
		PYBINDLIBRARY_EXPORTS _WINDOWS _USRDLL _UNICODE __WXMSW__ 
		WXUSINGDLL _CRT_SECURE_NO_WARNINGS _SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)


find_package(wxWidgets REQUIRED core base)

target_include_directories(${PROJECT_NAME} PRIVATE ${wxWidgets_INCLUDE_DIRS})

target_link_directories(${PROJECT_NAME} PRIVATE 
						${CMAKE_SOURCE_DIR}/libs 
						${PYHOME}/libs)

target_link_libraries(${PROJECT_NAME}  
						${wxWidgets_LIBRARIES} 
						python3 
						${PYLIB} 
						scisuit_core 
						scisuit_plotter)


set( REQUIREDDLLS
	${CMAKE_SOURCE_DIR}/libs/scisuit_core.dll
	${CMAKE_SOURCE_DIR}/libs/scisuit_plotter.dll
	${CMAKE_SOURCE_DIR}/libs/${VARPY}.dll)

foreach( file_i ${REQUIREDDLLS})
	add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy 
	${file_i} ${CMAKE_SOURCE_DIR}/pythonpkg/scisuit/)
endforeach(file_i)