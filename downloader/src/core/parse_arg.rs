use std::path::PathBuf;

use reqwest::Url;

/*
from: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md
值	含义	备注
6	240P 极速	仅 MP4 格式支持仅platform=html5时有效
16	360P 流畅
32	480P 清晰
64	720P 高清	WEB 端默认值B站前端需要登录才能选择，但是直接发送请求可以不登录就拿到 720P 的取流地址 无 720P 时则为 720P60
74	720P60 高帧率	登录认证
80	1080P 高清	TV 端与 APP 端默认值 登录认证
112	1080P+ 高码率	大会员认证
116	1080P60 高帧率	大会员认证
120	4K 超清	需要fnval&128=128且fourk=1 大会员认证
125	HDR 真彩色	仅支持 DASH 格式 需要fnval&64=64 大会员认证
126	杜比视界	仅支持 DASH 格式 需要fnval&512=512
大会员认证
127	8K 超高清	仅支持 DASH 格式需要fnval&1024=1024 大会员认证
*/
pub fn is_valid_id(s: &str) -> bool {
    return s.starts_with("BV1") || s.starts_with("ep") || s.starts_with("ss");
}

pub fn parse(id_or_url: &str) -> Option<String> {
    if let Ok(url_obj) = Url::parse(id_or_url) {
        let path = PathBuf::from(url_obj.path());
        let s = path.file_name()?.to_str()?.to_string();

        if is_valid_id(&s) {
            return Some(s);
        }
    } else {
        println!()
    }

    None
}
