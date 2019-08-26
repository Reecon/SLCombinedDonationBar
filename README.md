# Combined Donation Bar

Progress bar for goals that combines streamlabs donations and cheers.

## Installation

* Download zip
* Import zip into bot
* Right-click script and select `Insert API Key`
* Click the `Copy HTML Path` button and add a local browser source in your streaming software with this path, or navigate to `C:\Users\[YOUR_USERNAME]\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts\SLCombinedDonationBar\Bar.html`

There are two goal bar overlays. The first, `Bar.html` uses the bot's event-system to react to cheers and donations. In order to be able to receive donation events the bot must be connected to Streamlabs with the streamer's account in the `Connections`-panel in lower left corner of the bot-ui.

The second option, `Bar2.html` directly connects to the Streamlabs API. To use this, you have to do the following:

* Rename `streamlabs_token.js.example` to `streamlabs_token.js` and open it in a text editor.
* Go to the Streamlabs website and navigate to `API Settings`. Select `API TOKENS` and copy `Your Socket API Token`.
* In the text editor replace `_SECRET_API_TOKEN_` with your API token.
* Save the file and edit the path to your browser source so it points to `Bar2.html` instead of `Bar.html`

__Note:__ Make sure the browser source does not get shut down when the scene it is in is inactive. It can not receive events when it is inactive and donations will not be counted towards the goal!

## Goal List

In order to keep maintainance low during streams, you can set up a list of goals which will automatically be cycled once the current goal is reached.
You can set a timer for how long the completed goal should stay before the switch occurs.

Amounts exceeding the current goal will be carried over to the new goal, including new donations that happen during the time between completion and switch.

You have several options for how the progress bar will behave when all goals are completed.

* Show Latest Donation or Cheer
* Repeat Last Goal Indefinitely
* Keep Last Goal Open Beyond 100%
* Make Random Goals

__Note:__ The browser source must be active, meaning the streaming software must be running and the source must be loaded, to make any changes to the goal list!

### Setting Up Multiple Goals

After you entered the data for a new goal, you can select the checkbox under the section `Goal List` to add the new goal at the end of the list.
When you save the settings, the new goal will be added and sent to the overlay.

You can set up as many goals as you want.

__Note:__ Adding the goal to the list takes priority over updating the current goal.

### Updating Goals

You can change the total and current amount of an existing goal by typing the goal title into the `Goal Title` field. If a goal with this title already exists,
the values for total and current amount will be saved for that goal.

__Note:__ The checkbox in the `Goal List` section must be active!

### Deleting Goals From The List

You can delete goals by typing the title of the goal you want to delete into the `Goal Title` field and set the `Total Amount` to `0`.

__Note:__ The checkbox in the `Goal List` section must be active!

### Importing Goals In Bulk From File

If you frequently have to handle many goals, using the previously described method of adding them one by one can get cumbersome pretty quickly. The script folder has a `CSV`-file called `bulk_goals.csv` which can be imported to set up multiple goals at once.

You can open this file in your system's default `CSV`-editor by clicking the `EDIT BULK FILE`-button in the `Util`-section of the script. The bot expects the values to be separated by semicolon `;` and does not expect the file to have a header. Each Line represents one goal in the following format:

```csv
test goal 1;1;10
test goal 2;0;234
test goal 3/3;22.23;100
```

Click the `IMPORT BULK DATA`-button to import the goals you have configured in the file. 

__Note:__ This will replace all goals currently added to the list!

## Styling

Based on Bootstrap CSS progress bars, the CSS classes for customization are:

```txt
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

div[is-full="true"] {
    background: green;
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
