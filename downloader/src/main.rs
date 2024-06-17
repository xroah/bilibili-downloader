use clap::Command;

mod cmd;

fn main() {
    let matches = cmd::create_cmd().get_matches();

    cmd::core::handle(&matches);
}
