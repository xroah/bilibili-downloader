use std::collections::HashSet;

use clap::ArgMatches;

use crate::{core, term::TermFgColor};

pub fn handle(matches: &ArgMatches) -> Vec<String> {
    let videos = matches.get_many::<String>("videos");
    let mut video_ids = HashSet::<String>::new();
    let print = |v: &str| println!("{}", format!("{v}: 地址无效").red());

    if let Some(videos) = videos {
        for v in videos {
            if v.starts_with("https") {
                if !v.contains("bilibili") {
                    print(v);

                    continue;
                }

                if let Some(id) = core::parse_arg::parse(v) {
                    video_ids.insert(id);
                } else {
                    print(v);
                }
            } else {
                if core::parse_arg::is_valid_id(v) {
                    video_ids.insert(v.clone());
                } else {
                    println!("{}", format!("{v}: ID不正确").red());
                }
            }
        }
    }

    video_ids.iter().map(|id| id.clone()).collect()
}
