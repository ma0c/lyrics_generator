# Installing Freeling from source in Ubuntu

```bash
sudo apt install python3-dev
sudo apt install \
    libboost-dev \
    libboost-regex-dev \
    libicu-dev \
    libboost-system-dev \
    libboost-program-options-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    zlib1g
    
git clone https://github.com/TALP-UPC/FreeLing
cd FreeLing
mkdir build && cd build
cmake .. -DPYTHON3_API=ON
sudo make -j 4 install
```

## Usage

```bash
PYTHONPATH=/usr/local/share/freeling/APIs/python3 python sample.py < text_sample.txt
```
