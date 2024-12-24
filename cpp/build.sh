#!/bin/bash

cmake -B build -S . -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=conan/conan_provider.cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=1
cmake --build build --config Release
