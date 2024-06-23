mod cmd;
mod encrypt;
mod core;
pub mod term;

fn main() {
    let matches = cmd::create_cmd().get_matches();

    cmd::main_cmd::handle(&matches);

    match matches.subcommand() {
        Some(("settings", settings_matches)) => {
            println!("Settings");
        }
        _ => {
            
        }
    }
}
