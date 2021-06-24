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

## Manually link to your virtualenv

```bash
ln -s /usr/local/share/freeling/APIs/python3/_pyfreeling.so ../.virtualenv/lib/python3.7/site-packages
cp /usr/local/share/freeling/APIs/python3/pyfreeling.py ../.virtualenv/lib/python3.7/site-packages/

```

## Usage

```bash
PYTHONPATH=/usr/local/share/freeling/APIs/python3 python sample.py < text_sample.txt
```
