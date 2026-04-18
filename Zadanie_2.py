#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def generate_i2c_diagram(slave_addr=0x08, data_byte=0x42):
    """
    Генерирует текстовую временную диаграмму I2C
    """
    # Преобразование адреса в 7-битную строку
    addr_bits = format(slave_addr, '07b')
    data_bits = format(data_byte, '08b')
    
    print("=" * 70)
    print("ВРЕМЕННАЯ ДИАГРАММА ОБМЕНА ПО ШИНЕ I2C")
    print(f"Master -> Slave (Адрес: 0x{slave_addr:02X}, Данные: 0x{data_byte:02X})")
    print("=" * 70)
    
    # Формирование строки SCL (тактовый сигнал)
    scl_line = "SCL: "
    for i in range(20):
        scl_line += "‾\_/" if i < 19 else "‾"
    print(scl_line)
    
    # Формирование строки SDA (данные)
    sda_line = "SDA: ‾\\"
    
    # Старт
    sda_line += "___/"
    
    # Адресные биты
    for bit in addr_bits:
        sda_line += f"‾‾‾\\" if bit == '1' else f"___/"
    sda_line += "‾‾‾\\"  # Бит W (0)
    sda_line += "_______/"  # ACK
    
    # Биты данных
    for bit in data_bits:
        sda_line += f"‾‾‾\\" if bit == '1' else f"___/"
    sda_line += "_______/"  # ACK
    sda_line += "‾‾‾\\"     # Стоп
    sda_line += "_______"   # Конец
    
    print(sda_line)
    
    print("\n" + "-" * 70)
    print("Обозначения:")
    print("  S   : Старт (SDA ↓ при SCL ↑)")
    print("  P   : Стоп  (SDA ↑ при SCL ↑)")
    print("  ACK : Подтверждение от Slave")
    print(f"  Адрес : 0x{slave_addr:02X} = {addr_bits} + W")
    print(f"  Данные: 0x{data_byte:02X} = {data_bits}")
    print("-" * 70)
    
    # Таблица расшифровки
    print("\nТакт | Сигнал SDA")
    print("-----+--------------------------------------------------")
    print("  1  | Старт (S)")
    for i, bit in enumerate(addr_bits, start=2):
        print(f"  {i}  | Адрес A{i-2} = {bit}")
    print(f"  {len(addr_bits)+2}  | R/W = 0 (Write)")
    print(f"  {len(addr_bits)+3}  | ACK (Slave)")
    for i, bit in enumerate(data_bits, start=len(addr_bits)+4):
        print(f"  {i}  | Данные D{i-(len(addr_bits)+4)} = {bit}")
    print(f"  {len(addr_bits)+len(data_bits)+4}  | ACK (Slave)")
    print(f"  {len(addr_bits)+len(data_bits)+5}  | Стоп (P)")

if __name__ == "__main__":
    # Генерация для нашего случая
    generate_i2c_diagram(slave_addr=8, data_byte=128)  # Пример с порогом >127
