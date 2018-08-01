Progress bar for goals that combines streamlabs donations and cheers.

### Installation

* Download zip
* Import zip into bot
* Right-click script and select `Insert API Key`
* Click the `Copy HTML Path` button and add a local borwser source in your streaming software with this path

There are two goal bar overlays. The first, `Bar.html` uses the bot's event-system to react to cheers and donations. In order to be able to receive donation events the bot must be connected to Streamlabs in the `Connections`-panel in lower left corner of the bot-ui.

The second option, `Bar2.html` directly connects to the Streamlabs API. To use this, you have to do the following:
* Open `Bar2.html` in a text editor
* Go to the Streamlabs website and navigate to `API Settings`. Select `API TOKENS` and copy `Your Socket API Token`.
* In the text editor go to line 31 and replace `_SECRET_API_TOKEN_` with your API token.
* Save the file and edit the path to your browser source so it points to `Bar2.html` instead of `Bar.html`


### Styling
Based on Bootstrap CSS progress bars, the CSS classes for customization are:

```
progress - the bootstrap progressbar
progress-bar - the bootstrap progressbar progress
title - the donation title
current - the current amount text
percent - the current percent text
goal - the goal text
```

Complete styling example:

```css
body {
    background-color: rgba(0, 0, 0, 0); 
    margin: 0px auto; 
    overflow: hidden; 
}

.progress {
    height: 50px;
    background: rgba(0,0,0,0.8);
    border-radius: 20%;
}

.progress-bar {
    background: royalblue;
    transition: width 3s ease-out;
}

.current {
    position: absolute;
    left: 20;
    color: white;
    font-size: 1.5em;
    font-weight: bold;
}

.current::before {
    content:'$';
}

.goal {
    position: absolute;
    right: 20;
    color: white;
    font-size: 1.5em;
    font-weight: bold;
}

.goal::before {
    content:'$';
}

.title {
    position: absolute;
    left: 50%;
    transform: translate(-50%, 0);
    text-shadow: 1px 1px 10px black;
    color: white;
    font-size: 2em;
    font-weight: bold;
}

.percent {
    position: relative;
    top: 22;
    color: red;
    font-size:1.5em;
}
```