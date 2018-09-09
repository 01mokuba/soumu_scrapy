# maff_scrapy

## setup and basic usage

`python 3.6.x` recommended.

1. clone this repository

```
git clone https://github.com/01mokuba/soumu_scrapy.git
cd maff_scrapy
```

2. install Scrapy

```
python -m venv .venv
source ./.venv/bin/activate
pip install scrapy
```

3. run the crawler

```
cd soumu_scrapy
scrapy crawl archive -o soumu.json --logfile soumu.log
```

The results saved in `soumu_scrapy/maff.json` and the log saved in `soumu_scrapy/maff.log`. Downloaded PDFs are saved in `soumu_scrapy/downloads/full`.
