g++ -O2 -o hamming74/sender hamming74/sender.cpp
python3 hamming74/receiver.py
python3 crc32/sender.py
g++ -O2 -o crc32/receiver crc32/receiver.cpp
tests/run_all.sh