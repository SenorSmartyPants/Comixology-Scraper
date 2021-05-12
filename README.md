# Comixology Scraper

Download zip from [Mylar](https://github.com/SenorSmartyPants/Comixology-Scraper/tree/mylar) or [ComicRack](https://github.com/SenorSmartyPants/Comixology-Scraper/tree/ComicRack) branches. Each one is tuned to work with the respective program.

Currently Comixology Scraper depends on some metadata already existing for the comic archive being scraped. This metadata is used to verify the match.

Edit config.py to change what is scraped and overwrite behavior.

I primarily use this to grab genres from comixology.

There is no progress bar yet in comicrack, just a pop up when finished. And also console output.

## Mylar setup

Files included here assume you are running Hotio's docker image of Mylar. If not you may need to adjust file paths.

Mount a volume for post processing scripts
```
    volumes:
      - /mnt/storage/scripts/comics:/scripts
```

Install mylar branch of Comixology scraper into ```/scripts/Comixology-Scraper```

Copy ```/scripts/Comixology-Scraper/mylar-wrapper.sh``` to ```/scripts/mylar-wrapper.sh```

You can use mylar-wrapper.sh to call multiple scripts, if you have them. But it works fine for one.

Enable 'Run script AFTER Post-Processing' in Mylar.

Extra script location ```/scripts/mylar-wrapper.sh```

Check ```Enable Metadata Tagging``` and ```Write ComicRack (cr) tags (ComicInfo.xml)``` in Mylar post processing. Comixology Scraper needs some info in ComicInfo.xml to run properly.

