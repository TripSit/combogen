## Dependencies
- Install [Python 3](https://www.python.org), [Node.js](https://nodejs.org), and [npm](https://www.npmjs.com).
- Afterwards make sure `python` (or `python3`), `node`, `npm` are in your `PATH`.
- Install required python modules: `pip3 install requests jinja2`

### Google Chrome
Some of the used npm packages may want to use Google Chrome or Chromium. If you need to install it depends on your operating system. It's not needed on macOS 13.4. for example.

After installing Chrome, make sure `google-chrome` or `chrome` are in your `PATH`.

### WSL and Chrome
[Follow these instructions on ow to install Google Chrome in WSL](https://scottspence.com/posts/use-chrome-in-ubuntu-wsl)!

## How to run
- `git clone` this repo
- `cd` to the project dir
- Run `npm install`
- Run `python -m combogen` (or `python3 -m combogen`)

## How to configure
- Edit **config.json**
- Edit the text in **/combogen/translations**

## Where do I find the chart?
- Run the script (see above)
- PNGs are located in output/png/
- PDFs are located in output/pdf/
