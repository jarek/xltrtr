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

function transliterationRequested() {
    var text = el('query').value;

    if (oldText !== text) {
        if (text === '') {
            showResult('&nbsp;');
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
    if (result.input !== currentRequest) {
        // ignore results that arrive out of order
        return;
    }

    var output = result.output;

    var topScore = output[0].score;
    var results = []
    for (var i = 0, l = output.length; i < l; i++) {
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

var oldText = '';
var currentRequest = '';
el('submit-button').onclick = transliterationRequested;
el('query').onkeyup = transliterationRequested;
el('query').focus();

