# Renameium

While using [Boboarr](https://github.com/iam4x/bobarr) I had some issues with certain files (in particular) tv shows not being renamed correctly. This could cause problems with Plex not recognizing and importing these files.

This script simply scans the bobarr database for new files, renames them appropriately, then updates the bobarr database. It is fully integrated with bobarr.

## Usage
```bash
pip install -r requirements.txt
python src/renameium.py
```

## Remaining Project Goals
- [x] MVP, is able to rename files automatically
- [ ] Integration with imdb, to provide the year/etc for files
- [ ] Improve configuration options
- [ ] Create some sort of automated testing suite

## Licensing and Contribution
Unless otherwise specified, all contributions will be licensed under MIT.