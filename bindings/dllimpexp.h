#pragma once

#ifdef PYBINDLIBRARY_EXPORTS
#define DLLPYBIND __declspec(dllexport)
#else
#define DLLPYBIND __declspec(dllimport)
#endif
