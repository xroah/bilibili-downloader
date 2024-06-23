use std::borrow::Borrow;
use std::error::Error;
use std::{cell::RefCell, collections::HashMap};

use reqwest::cookie::Cookie;
use reqwest::{
    header::{HeaderMap, HeaderName, HeaderValue, COOKIE, ORIGIN, REFERER, USER_AGENT},
    Client, Method, Response,
};

use crate::encrypt::{self};

static USER_AGENT_STR: &str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62";
static HOST: &str = "https://www.bilibili.com";

type Query = HashMap<&'static str, Box<dyn ToString>>;
type JsonResult = Result<serde_json::Value, Box<dyn Error>>;
type ResResult = Result<Response, Box<dyn Error>>;

pub struct Req {
    count: u8,
    is_encrypt: bool,
    cookie: RefCell<String>,
}

impl Req {
    const MAX_RETRIES: u8 = 10;

    pub fn new(is_encrypt: bool) -> Self {
        Self {
            count: 0,
            is_encrypt,
            cookie: RefCell::new(String::new()),
        }
    }

    fn qs(query: &Query, is_encrypt: bool) -> Vec<(String, String)> {
        let mut ret = Vec::new();
        let mut map = HashMap::new();

        for (k, v) in query {
            ret.push((k.to_string(), v.to_string()));
            map.insert(*k, v.to_string());
        }

        if is_encrypt {
            let encrypted = encrypt::enc_wbi(map);

            for (k, v) in encrypted {
                ret.push((v, k));
            }
        }

        ret
    }

    async fn do_req(
        &self,
        m: Method,
        url: &str,
        query: Option<Query>,
        headers: Option<Vec<(HeaderName, &str)>>,
    ) -> ResResult {
        let mut query_vec = Vec::<(String, String)>::new();
        let mut header_map = HeaderMap::new();

        if let Some(query) = query {
            query_vec = Self::qs(&query, self.is_encrypt);
        }

        if let Some(headers) = headers {
            for (n, s) in headers {
                let value = HeaderValue::from_str(&s).unwrap();

                header_map.insert(n, value);
            }
        }

        let res = Client::new()
            .request(m.clone(), url)
            .query(&query_vec)
            .headers(header_map.clone())
            .send()
            .await?;

        Ok(res)
    }

    async fn get_cookie(&self) {
        if !self.cookie.borrow().is_empty() {
            return;
        }

        let mut ret = Vec::<String>::new();
        let res = self.do_req(Method::GET, HOST, None, None).await;

        if let Ok(res) = res {
            let cookies = res.cookies();

            for c in cookies {
                ret.push(format!("{}={}", c.name(), c.value()));
            }
        }

        *self.cookie.borrow_mut() = ret.join(";");
    }

    pub async fn get(&self, url: &str, query: Query) -> JsonResult {
        self.get_cookie().await;

        let cookie = self.cookie.borrow();
        let headers = vec![
            (REFERER, HOST),
            (ORIGIN, HOST),
            (USER_AGENT, USER_AGENT_STR),
            (COOKIE, cookie.as_str()),
        ];

        let res = self
            .do_req(Method::GET, url, Some(query), Some(headers))
            .await?
            .text()
            .await?;
        let json = serde_json::from_str::<serde_json::Value>(&res)?;

        Ok(json)
    }
}
