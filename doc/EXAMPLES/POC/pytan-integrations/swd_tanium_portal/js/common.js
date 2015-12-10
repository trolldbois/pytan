function newwindow(url, title, options)
{
// for some reason, this works better when it's in a separate function
window.open(url, title, options);
}

function popupmessage(title, msg) {
    newWindow = window.open('', title, 'scrollbars,resizable,width=628,height=333');
    var tmp = newWindow.document;
    tmp.write('<html><head>\n<title>' + title + '</title>\n');
    tmp.write('<link rel="stylesheet" type="text/css" href="css/app.css">\n');
    tmp.write('</head><body oncontextmenu="return false;"><p>\n');
    tmp.write('<h1>' + title + '</h1><p>\n');
    tmp.write(msg);
    tmp.write('</p>\n<p><br>\n<button onclick="javascript:self.close(); return false;">Close</button></p>\n');
    tmp.write('</body></html>\n');
    tmp.close();
}

$(function(){
	if (document.location.href.indexOf('showhidden=yes') > 0)
		$(".hidden_output").show();
	});
