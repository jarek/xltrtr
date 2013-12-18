/*notmuchhere*/

function xhrJSON(url, callback) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function () {
        callback(JSON.parse(this.responseText));
    };
    xmlhttp.open("GET",url);
    xmlhttp.send();
}

function el(id) {
    return document.getElementById(id);
}

if (typeof String.prototype.startsWith !== 'function') {
    String.prototype.startsWith = function (prefix){
        return this.slice(0, prefix.length) == prefix;
    };
}

function transliterationRequested() {
    var text = el('query').value;

    if (oldText !== text) {
        if (text === '') {
            // "show" empty result
            showResult();
        } else {
            currentRequest = text;
            var form = el('transliteration-form');
            var url = form.action + '?query=' + text + '&ajax=1';
            result = xhrJSON(url, showResult);
        }
    }

    oldText = text;

    return false;
}

function showResult(result) {
    if (!result) {
        // show empty result
        el('translation').innerHTML = '';
        el('query').focus();
        currentResultIsFor = '';
        return;
    }

    if (result.input !== currentRequest 
        && !(currentRequest.startsWith(result.input) 
            && result.input.startsWith(currentResultIsFor))) {
        // ignore results that arrive out of order
        return;
    }

    currentResultIsFor = result.input;
    newState = {}; // TODO: store state?
    newUrl = location.href.split('?')[0] + '?query=' + result.input;
    newTitle = document.title + ' for ' + result.input;
    history.pushState(newState, newTitle, newUrl);
    // TODO: handle popstate to handle back button correctly

    var output = result.output;

    var topScore = output[0].score;
    var results = [];
    for (var i in output) {
        if (output[i].score === topScore) {
            results.push(formatLang(output[i]));
        }
    }

    el('translation').innerHTML = results.join(' or ');

    el('query').focus();
}

function formatLang(result) {
    var template = document.getElementById('translationtemplate');
    if (!template) return '';

    template = template.innerHTML;

    return template.replace(/{result}/g, result.output)
        .replace(/{lang}/g, result.lang)
        .replace(/{iso}/g, result['iso639-1']);
}

// TODO: detect XMLHttpRequest and document.getElementById and fail gracefully

// TODO: after each keystroke, start a 100-200 ms timer during which
// new keystrokes won't cause additional requests. after expiry of timer
// we can send a request, if there are further keystrokes they're subject
// to a timer again. basically send a request every 100-200 ms max.

var oldText;
var currentRequest;
var currentResultIsFor = '';
el('submit-button').onclick = transliterationRequested;
el('query').onkeyup = transliterationRequested;
el('query').focus();

