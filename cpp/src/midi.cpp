#include "midi.hpp"
#include <fmt/format.h>
#include <iomanip>
#include <sstream>

using namespace libremidi;

auto find_target_port( const auto &ports, const std::string &target_name )
{
    for( auto &port : ports )
    {
        if( port.device_name == target_name )
        {
            fmt::println( "port {} - {} - {}", port.port_name, port.device_name, port.display_name );
            return port;
        }

    }

    return ports.at( 0 );
}

input_port find_input( const std::string &name )
{
    libremidi::observer observer( { .track_virtual = true } );
    auto ports = observer.get_input_ports();
    return find_target_port( ports, name );
}

output_port find_output( const std::string &name )
{
    libremidi::observer observer( { .track_virtual = true } );
    auto ports = observer.get_output_ports();
    return find_target_port( ports, name );
}

midi_ports find_in_out_pair( const std::string &name )
{
    return
    {
        find_input( name ),
        find_output( name )
    };
}

midi_pair open_in_out_pair(
    const std::string &name,
    const input_configuration& input_configuration,
    const output_configuration& output_configuration )
{
    auto ports = find_in_out_pair( name );

    midi_pair io = {
        midi_in( input_configuration ),
        midi_out( output_configuration )
    };

    io.input.open_port( ports.input );
    io.output.open_port( ports.output  );

    return io;
}

std::string to_string( const std::span< unsigned char > &data )
{
    std::stringstream str;

    bool first = true;
    str << "{";

    for( auto value : data )
    {
        str << (first ? " " : ", ") << "0x"
            << std::hex << std::setw( 2 ) << std::setfill( '0' )
            << static_cast< unsigned int >( value );
        first = false;
    }

    str << " }";

    return str.str();
}
