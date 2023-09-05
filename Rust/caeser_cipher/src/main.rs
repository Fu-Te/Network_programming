extern crate caesar;

fn main() {
    // 暗号化と復号化 --- (*1)
    let text = "I LOVE YOU.";
    let enc_text = caeser(&text, 3); // 暗号化
    let dec_text = caesar(&enc_text, -3); // 復号化
    println!("文字列: {}", text);
    println!("暗号化: {}", enc_text);
    println!("復号化: {}", dec_text);
}
