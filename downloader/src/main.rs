use std::collections::HashMap;

use request::Req;

mod cmd;
mod core;
mod encrypt;
mod request;
mod term;

#[tokio::main]
async fn main() {
    let matches = cmd::create_cmd().get_matches();
    let ids = cmd::main_cmd::handle(&matches);

    if ids.len() > 0 {
        let query_vec: Vec<(&str, Box<dyn ToString>)> = vec![
            ("platform", Box::new("web")),
            ("bvid", Box::new(ids[0].clone())),
        ];
        let req = Req::new(true);
        let value = req
            .get(
                "https://api.bilibili.com/x/web-interface/wbi/view/detail",
                HashMap::from_iter(query_vec),
            )
            .await;

        println!("{value:?}");
    }

    match matches.subcommand() {
        Some(("login", settings_matches)) => {
            println!("Login");
        }
        _ => {}
    }
}
