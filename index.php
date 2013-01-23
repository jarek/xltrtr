<?php

$input = $_GET['input'];

$EtoRlower = array(
	'\'' => 'ь',
	'yu' => 'ю',
	'ju' => 'ю',
	'yo' => 'ё',
	'jo' => 'ё',
	'ya' => 'я',
	'ja' => 'я',
	'ye' => 'е',
	'je' => 'е',
	'a' => 'а',
	'b' => 'б',
	'v' => 'в',
	'w' => 'в',
	'g' => 'г',
	'd' => 'д',
	'e' => 'е',
	'ż' => 'ж',
	'zh' => 'ж',
	'z' => 'з',
	'i' => 'и',
	'j' => 'й',
	'k' => 'к',
	'l' => 'л',
        'ł' => 'л',
	'm' => 'м',
	'n' => 'н',
	'o' => 'о',
	'p' => 'п',
	'r' => 'р',
	's' => 'с',
	't' => 'т',
	'u' => 'у',
	'f' => 'ф',
	'h' => 'х',
	'c' => 'ц',
	'ch' => 'ч', 'ć' => 'ч',
	'sh' => 'ш', 'sz' => 'ш',
	'sch' => 'щ', 'shch' => 'щ', 'szcz' => 'щ',
	'y' => 'ы'
	);

foreach($EtoRlower as $e => $r) {
	$EtoRupper[mb_strtoupper($e, 'utf-8')] = mb_strtoupper($r, 'utf-8');
}

$trans = array_merge($EtoRupper, $EtoRlower,
		array_flip($EtoRupper), array_flip($EtoRlower));

$output = strtr($input, $trans);

if (isset($_GET['ajax'])) {
	header('Content-type: text/html; charset=utf-8');
	die($output);
}

?><!doctype html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>xltrtr</title>

<style type="text/css">
body		{ background: #fff; color: #222; font-family: trebuchet ms, serif; }
#translation	{ font-size: 200%; }
</style>

<form>
<fieldset>
<legend>input</legend>
<p><input type="text" name="input" id="input" value="<?=$_GET['input'];?>" onkeyup="textChanged(event);">
<input type="submit" value="submit" onclick="transliterate(); return false;">
</fieldset>
</form>

<fieldset>
<legend>output</legend>
<p><span id="translation"><?=$output; ?></span>

<p><input type="text" id="translation2" value="<?=$output; ?>">

<a id="google-link" href="http://translate.google.com/#auto|en|<?=$output;?>">google translate</a>
<a id="wt-en-link" href="http://en.wiktionary.org/wiki/<?=$output; ?>">wt en</a>
<a id="wt-pl-link" href="http://pl.wiktionary.org/wiki/<?=$output; ?>">wt pl</a>
<a id="wt-ru-link" href="http://ru.wiktionary.org/wiki/<?=$output; ?>">wt ru</a>
</fieldset>

<p><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/6/60/KB_Russian.svg/800px-KB_Russian.svg.png" alt="The Russian keyboard layout." title="Learn this.">

<script type="text/javascript">
/*notmuchhere*/

function loadTransliteration(url) {
	xmlhttp=new XMLHttpRequest();
	xmlhttp.open("GET",url,false);
	xmlhttp.send(null);
	return xmlhttp.responseText;
}

function makeWiktionaryLink(word, language) {
	return 'http://' + language + '.wiktionary.org/wiki/' + word;
}

function makeGoogleTranslateLink(word) {
	return 'http://translate.google.com/#auto|en|' + word;
}

function getEl(id) {
	return document.getElementById(id);
}

var ajaxTimer = 0;
var oldText = "";

function textChanged(event) {
	if (oldText != getEl('input').value) {
		ajaxTimer = 1;	// trigger

		if (getEl('translation').innerHTML.substr(-3, 3) != '...')
		{
			getEl('translation').innerHTML += '...';
		}
	}

	oldText = getEl('input').value;
}

function textClock() {
	if (ajaxTimer > 0) {
		if (ajaxTimer < 3) {
			ajaxTimer = ajaxTimer + 1;
		} else {
			ajaxTimer = 0; // reset once sent
			transliterate();
		}
	}
}

function transliterate() {
	input = getEl('input').value;

	result = loadTransliteration('?input=' + input + '&ajax=1');

	getEl('translation').innerHTML = result;
	getEl('translation2').value = result;
	
	getEl('google-link').href = makeGoogleTranslateLink(result);
	
	getEl('wt-en-link').href = makeWiktionaryLink(result, 'en');
	getEl('wt-pl-link').href = makeWiktionaryLink(result, 'pl');
	getEl('wt-ru-link').href = makeWiktionaryLink(result, 'ru');
}

setInterval('textClock()', 300);
getEl('input').focus();
</script>
