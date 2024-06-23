pub trait TermFgColor {
    fn red(&self) -> String;
    fn cyan(&self) -> String;
    fn black(&self) -> String;
    fn white(&self) -> String;
    fn blue(&self) -> String;
}

fn colorize(s: &str, fg: u8) -> String {
    format!("\x1b[{fg}m{s}\x1b[0m")
}

impl TermFgColor for String {
    fn red(&self) -> String {
        colorize(self, 31)
    }

    fn cyan(&self) -> String {
        colorize(self, 36)
    }

    fn black(&self) -> String {
        colorize(self, 30)
    }

    fn white(&self) -> String {
        colorize(self, 37)
    }

    fn blue(&self) -> String {
        colorize(self, 34)
    }
}
