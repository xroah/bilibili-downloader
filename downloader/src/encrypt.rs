use std::{
    collections::HashMap,
    hash::RandomState,
    time::{SystemTime, UNIX_EPOCH},
};

use md5::{Digest, Md5};

static IMG_KEY: &str = "7cd084941338484aae1ad9425b84077c";
static SUB_KEY: &str = "4932caff0ff746eab6f01bf08b70ac45";

pub fn get_mixin_key(key: &str) -> String {
    let chars = key.chars().collect::<Vec<char>>();

    vec![
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19,
        29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
        22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
    ]
    .iter()
    .map(|&n| {
        let c = chars[n] as u8;

        unsafe { String::from_utf8_unchecked(vec![c]) }
    })
    .collect::<Vec<String>>()
    .join("")[..32]
        .to_owned()
}

fn encode(value: &str) -> String {
    let bytes = value.as_bytes();
    let exclusions = "!-()~.*_'";
    let mut ret = String::new();

    for b in bytes {
        if !b.is_ascii_alphanumeric() && !exclusions.contains(*b as char) {
            ret.push_str(&format!("%{b:X}"));
        } else {
            ret.push(*b as char);
        }
    }

    ret
}

pub fn enc_wbi(query_map: HashMap<&str, String>) -> HashMap<String, String> {
    let mut ret = HashMap::new();
    let mut query_map: HashMap<String, String, RandomState> = HashMap::from_iter(
        query_map
            .iter()
            .map(|(&k, v)| (k.to_string(), v.clone())),
    );
    let key = format!("{IMG_KEY}{SUB_KEY}");
    let key = get_mixin_key(&key);
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
        .to_string();

    query_map.insert("wts".to_string(), now.clone());

    let mut keys = query_map.keys().collect::<Vec<&String>>();
    let mut to_bo_enc = Vec::new();

    keys.sort();

    for k in keys {
        to_bo_enc.push(format!("{}={}", encode(k), encode(&query_map[k])));
    }

    to_bo_enc.push(key);

    let mut hash = Md5::new();
    let mut md5_string = String::new();
    let bytes;

    hash.update(to_bo_enc.join("&"));

    bytes = hash.finalize().to_vec();

    for b in bytes {
        md5_string.push_str(&format!("{:x}", b))
    }

    ret.insert("w_rid".to_string(), md5_string);
    ret.insert("wts".to_string(), now);

    ret
}
