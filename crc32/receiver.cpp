#include <iostream>
#include <vector>
#include <string>
#include <bitset>
#include <cstdint>

uint32_t crc32(const std::vector<uint8_t>& data) {
    static uint32_t table[256];
    static bool init = false;
    if (!init) {
        for (uint32_t i = 0; i < 256; ++i) {
            uint32_t c = i;
            for (int j = 0; j < 8; ++j)
                c = (c & 1) ? (0xEDB88320u ^ (c >> 1)) : (c >> 1);
            table[i] = c;
        }
        init = true;
    }
    uint32_t crc = 0xFFFFFFFFu;
    for (uint8_t b : data)
        crc = table[(crc ^ b) & 0xFF] ^ (crc >> 8);
    return crc ^ 0xFFFFFFFFu;
}

std::string bits_to_text(const std::string& bits) {
    std::string text;
    for (size_t i = 0; i + 7 < bits.size(); i += 8) {
        std::string byte = bits.substr(i, 8);
        char c = static_cast<char>(std::stoi(byte, nullptr, 2));
        text.push_back(c);
    }
    return text;
}

int main() {
    std::string in;
    if (!(std::cin >> in)) return 0;

    std::cout << "[DEBUG] Longitud trama recibida: " << in.size() << " bits\n";

    if (in.size() < 32) {
        std::cerr << "Trama muy corta\n";
        return 1;
    }

    std::string msg_bits = in.substr(0, in.size() - 32);
    std::string recv_crc_bits = in.substr(in.size() - 32);

    std::vector<uint8_t> bytes;
    for (size_t i = 0; i < msg_bits.size(); i += 8) {
        std::string chunk = msg_bits.substr(i, 8);
        if (chunk.size() < 8) chunk = std::string(8 - chunk.size(), '0') + chunk;
        bytes.push_back(static_cast<uint8_t>(std::stoi(chunk, nullptr, 2)));
    }

    uint32_t calc = crc32(bytes);
    std::string calc_bits = std::bitset<32>(calc).to_string();

    if (calc_bits == recv_crc_bits) {
        std::cout << "Sin errores. Trama OK.\n";
        std::cout << "Mensaje decodificado: " << bits_to_text(msg_bits) << "\n";
    } else {
        std::cout << "Error detectado. Se descarta.\n";
        std::cout << "CRC recv: " << recv_crc_bits << " | CRC calc: " << calc_bits << "\n";
    }
    return 0;
}