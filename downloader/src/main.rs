use std::collections::HashMap;

mod cmd;
mod encrypt;

fn main() {
    let matches = cmd::create_cmd().get_matches();

    cmd::core::handle(&matches);

    encrypt::enc_wbi(HashMap::from([
        ("ids", "2837,2836,2870,2953,2954,2955,2956,5672"),
        ("pf", "0"),
    ]));
}
