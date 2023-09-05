pub fn caeser_encrypt(text: &str, shift: i16) -> String {
    let a_code = 'A' as i16;
    let z_code = 'Z' as i16;

    let mut result = String::new();

    for ch in text.chars() {
        //小文字を大文字に変換
        let ch = if ch.is_lowercase() {
            ch.to_ascii_uppercase()
        } else {
            ch
        };
        let code = ch as i16;

        if a_code <= code && code <= z_code {
            let mut enc = (code - a_code + shift + 26) % 26 + a_code;
            enc = enc as char;
            result.push(enc);
        } else {
            result.push(ch);
        }
    }
    return result;
}
