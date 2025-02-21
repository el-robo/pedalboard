#include <algorithm>
#include <array>
#include <cstdio>
#include <fmt/base.h>
#include <fmt/format.h>
#include <chrono>
#include <iomanip>
#include <libremidi/message.hpp>
#include <sstream>
#include <thread>

#include "midi.hpp"
#include "toneprint.hpp"

using namespace libremidi;
using namespace std::chrono_literals;
using namespace toneprint;

enum class event
{
    probe = 0x03,
    ping = 0x05,
    state = 0x08,
    query = 0x09,
    start_preset = 0x1E,
    preset = 0x0D,
    foot = 0x0F
};

const auto toneprint_name = "WINE midi driver";
const auto hof_name = "HOF 2";
const auto client_name = "toneprint-capture";

void send( midi_out &output, const libremidi::message &message )
{
    output.send_message( message );
    std::this_thread::sleep_for( 10ms );
}

int main( int argc, char **argv )
{
    fmt::println( "Please start TonePrint before connecting the Hall of Fame USB cable" );

    std::optional< midi_pair > toneprint;
    std::optional< midi_pair > hof;

    hof = open_in_out_pair( hof_name,
        {
            .on_message = [ & ]( message &&message )
            {
                if( message.size() < preamble.size() + 2 || !std::equal( preamble.begin(), preamble.end(),  message.begin() + 1 ) )
                {
                    fmt::println( "unmatched: {}", to_string(  std::span( message.begin(), message.end() ) ) );
                    return;
                }

                const auto body = std::span< unsigned char >( message.begin() + 6, message.begin() + message.size() - 1 );

                switch( toneprint::event( body[ 0 ] ) )
                {
                    case toneprint::event::probe:
                    case toneprint::event::query:
                    case toneprint::event::ping:
                        // these only come from toneprint which connected here
                        return;

                    default:
                        fmt::println( "send( output, {} );", to_string( body ) );
                        toneprint->output.send_message( message );
                        break;
                }


            },
            .on_error = [] ( auto error, const source_location& )
            {
                fmt::println( "hof error: {}", error );
            },
            .ignore_sysex = false,
            .ignore_timing = true,
            .ignore_sensing = true
        },
        {}
    );

    toneprint = open_in_out_pair( toneprint_name,
        {
            .on_message = [ & ]( message &&message )
            {
                if( message.size() < preamble.size() + 2 || !std::equal( preamble.begin(), preamble.end(),  message.begin() + 1 ) )
                {
                    fmt::println( "unmatched: {}", to_string(  std::span( message.begin(), message.end() ) ) );
                    return;
                }

                const auto body = std::span( message.begin() + 6, message.begin() + message.size() - 1 );
                fmt::println( "toneprint: {}", to_string( body ) );
                hof->output.send_message( message );
            },
            .on_error = [] ( auto error, const source_location& )
            {
                fmt::println( "toneprint error: {}", error );
            },
            .ignore_sysex = false,
            .ignore_timing = true,
            .ignore_sensing = true,
        }
    );

    fmt::print( "starting\n" );

    int c;
    while ((c = getchar()) != '\n' && c != EOF)
    {

    }

    fmt::print( "done\n" );
    return 0;
}
