# combogen

Combogen is an application that generates drug combo charts as PNG and PDF files to help users know the results and safety of drug combinations.

This repository does not contain the raw combination data, it is a simple image/PDF generator. The data is fetched from the [TripSit/drugs](https://github.com/TripSit/drugs) repository ([drugs.json](https://github.com/TripSit/drugs/blob/main/drugs.json)).

Output example (uses historamical data, not up to date):
![Example output](https://wiki.tripsit.me/images/3/3a/Combo_2.png)

## Dependencies
- Install [Python 3](https://www.python.org), [Node.js](https://nodejs.org), and [npm](https://www.npmjs.com).
- Afterwards make sure `python` (or `python3`), `node`, `npm`, `pip` are in your `PATH`.
- Move into the project directory using `cd`
- Create a virtual environment: `python3 -m venv venv`
- Install the required Python packages: `./venv/bin/pip3 install -r requirements.txt`

### Google Chrome
Some of the used npm packages may want to use Google Chrome or Chromium. If you need to install it depends on your operating system. It's not needed on macOS 13.4. for example.

After installing Chrome, make sure `google-chrome` or `chrome` are in your `PATH`.

### WSL and Chrome
[Follow these instructions on ow to install Google Chrome in WSL](https://scottspence.com/posts/use-chrome-in-ubuntu-wsl)!

## How to run
- `git clone` this repo
- `cd` to the project dir
- Run `npm install`
- Run `./venv/bin/python3 -m combogen`

## How to configure
- Edit **config.json**
- Edit the text in **/combogen/translations**

## Where do I find the chart?
- Run the script (see above)
- PNGs are located in output/png/
- PDFs are located in output/pdf/

## Troubleshooting common issues

### Result shows NXDRUG instead of real info

This means that the drug is not defined in the source json that the app uses to generate the chart.
The drug was most likely renamed/changed by accident in the [source data](https://github.com/TripSit/drugs/blob/main/drugs.json) or this project.
Check the lastest commit in the project to see if there was any breaking change made.
Please report the issue on our [Discord](https://discord.gg/tripsit).
You can use an older version of [drugs.json](https://github.com/TripSit/drugs/blob/main/drugs.json) as a temporary fix, simply edit the source in `config.json`.

## Contibuting

The easiest way to contribute is to translate the chart into your language.
You may find the translation data in the `combogen/translations/` directory.
Please use common (not complex) language and drug names to make the chart easily understandable by everyone.

## Licensing

Big thanks to everyone who contributed—this project wouldn’t be what it is without your help!

---

This project is licensed under the **PolyForm Noncommercial License**. Here is a (non legally binding TL;DR, find the full licence in the `LICENSE` file): *You can use, modify, and share this project freely **for noncommercial purposes only**. Any commercial use requires a separate license. Use by any charitable organization, educational institution, public research organization, public safety or health organization, environmental protection organization, or government institution is considered a permitted purpose **regardless of funding sources**. The project is provided **as-is**, with no warranties, and you must include this license if you redistribute it.*
