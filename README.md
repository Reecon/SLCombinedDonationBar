Progress bar for goals that combines streamlabs donations and cheers.

Insert API-Key after initial import.

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
```
body {
    background-color: rgba(0, 0, 0, 0); 
    margin: 0px auto; 
    overflow: hidden; 
}

.progress {
    height: 50px;
}

.progress-bar {
    background: linear-gradient(to right, red,orange,yellow,green,blue,indigo,violet);
}

.title {
    position: absolute;
    left: 50%;
    transform: translate(-50%, 0);
    text-shadow: 1px 1px 10px black;
    color: red;
    font-size: 2em;
    font-weight: bold;
}

.current {
    position: absolute;
    left: 0;
    color: black;
    font-size: 1.5em;
    font-weight: bold;
}

.percent {
    position: relative;
    top: 22;
    color: red;
    font-size:1.5em;
}

.goal {
    position: absolute;
    right: 0;
    color: black;
    font-size: 1.5em;
    font-weight: bold;
}
```