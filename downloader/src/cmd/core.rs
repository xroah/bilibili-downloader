use std::path::{Path, PathBuf};

use clap::ArgMatches;
use reqwest::Url;

fn parse(id_or_url: &str) {
    if let Ok(url_obj) = Url::parse(id_or_url) {
        let path = PathBuf::from(url_obj.path());

        println!("{:?}", path.file_name().unwrap());
    }
}

pub fn handle(matches: &ArgMatches) {
    let videos = matches.get_many::<String>("videos");

    if let Some(videos) = videos {
        for v in videos {
            if v.starts_with("http") {
                parse(v);
            } else {
                println!("{v}");
            }
        }
    }
}
