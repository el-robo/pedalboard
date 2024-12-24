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

add_executable( capture_preset
    capture.cpp
)

target_link_libraries( capture_preset PRIVATE fmt::fmt libremidi )
