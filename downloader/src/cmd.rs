use clap::{Arg, Command};

pub mod core;

pub fn create_cmd() -> Command {
    Command::new("bilibili下载器")
        .version(env!("CARGO_PKG_VERSION"))
        .arg(
            Arg::new("videos")
                .num_args(1..=10)
                .required(true)
                .help("视频地址或者id(bvid, epid, seasonid不支持avid)，多个以空格分隔"),
        )
        .subcommand(Command::new("settings").about("设置"))
}
