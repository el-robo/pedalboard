cmake_minimum_required( VERSION 3.31 )
project( pedalboard )

include( FetchContent )
find_package( fmt REQUIRED )

FetchContent_Declare(
    libremidi
    GIT_REPOSITORY https://github.com/celtera/libremidi
    GIT_TAG master
)

FetchContent_MakeAvailable(libremidi)

set( CMAKE_CXX_STANDARD 20 )

add_library( midi STATIC src/midi.cpp )
target_include_directories( midi PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_link_libraries( midi PUBLIC libremidi fmt::fmt )

add_executable( capture_preset
    src/capture.cpp
)

target_include_directories( capture_preset PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_link_libraries( capture_preset PRIVATE fmt::fmt midi )

add_executable( bridge
    src/bridge.cpp
)

# target_include_directories( bridge PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include )
target_link_libraries( bridge PRIVATE fmt::fmt midi )
