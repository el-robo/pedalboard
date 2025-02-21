#pragma once
#include <libremidi/libremidi.hpp>
#include <libremidi/observer_configuration.hpp>
#include <string>

libremidi::input_port find_input( const std::string &name );
libremidi::output_port find_output( const std::string &name );

struct midi_ports
{
    libremidi::input_port input;
    libremidi::output_port output;
};

midi_ports find_in_out_pair( const std::string &name );

struct midi_pair
{
    libremidi::midi_in input;
    libremidi::midi_out output;
};

midi_pair open_in_out_pair(
    const std::string &name,
    const libremidi::input_configuration& input_configuration = {},
    const libremidi::output_configuration& output_configuration = {}
);

std::string to_string( const std::span< unsigned char > &data );
