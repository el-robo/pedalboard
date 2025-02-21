#pragma once
#include <array>

namespace toneprint
{
    constexpr auto hall_of_fame_2 = 0x21;
    constexpr std::array< unsigned char, 5 > preamble =
    {
        0x00, 0x20, 0x1F, 0x00, hall_of_fame_2
    };

    enum class event : unsigned char
    {
        probe = 0x03,
        ping = 0x05,
        state = 0x08,
        query = 0x09,
        start_preset = 0x1E,
        preset = 0x0D,
        foot = 0x0F
    };

}
