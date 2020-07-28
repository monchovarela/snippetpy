var wrapper = document.getElementById('wrapper');
if (wrapper) {

    var loadWindow = function ($mode, $id) {
        // init codemirror
        var editor = CodeMirror.fromTextArea(document.getElementById($id), {
            lineNumbers: true,
            lineWrapping: true,
            autofocus: false,
            autoCloseBrackets: true,
            matchBrackets: false,
            tabMode: 'indent',
            mode: $mode,
            theme: 'darkpastel'
        });
        editor.setOption("extraKeys", {
            Tab: function (cm) {
                var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
                cm.replaceSelection(spaces);
            }
        });

        wrapper.classList.add('loaded');

        return editor;
    }


    // Html mode
    $htmlmode = 'text/html';
    var editor_html = loadWindow($htmlmode, 'html');

    //Css mode
    $cssmode = 'text/css';
    var editor_css = loadWindow($cssmode, 'css');

    //Js mode
    var $jsmode = 'text/typescript-jsx';
    var editor_js = loadWindow($jsmode, 'javascript');

    emmetCodeMirror(editor_html);
    Inlet(editor_css);


    var setElementSize = function (elem, full) {
        if (full) {
            elem.setSize(null, window.innerHeight - 25);
        } else {
            elem.setSize(null, window.innerHeight / 3 - 32);
        }
    }


    var toogleSize = function (elem, type) {
        elem.classList.toggle('isFull');
        if (elem.classList.contains('isFull')) {
            if (type === 'html') {
                setElementSize(editor_html, true);
                css_content.style.display = 'none';
                js_content.style.display = 'none';
            } else if (type === 'css') {
                setElementSize(editor_css, true);
                html_content.style.display = 'none';
                js_content.style.display = 'none';
            } else if (type === 'js') {
                setElementSize(editor_js, true);
                html_content.style.display = 'none';
                css_content.style.display = 'none';
            }
        } else {
            if (type === 'html') {
                setElementSize(editor_html);
                css_content.style.display = 'block';
                js_content.style.display = 'block';
            } else if (type === 'css') {
                setElementSize(editor_css);
                html_content.style.display = 'block';
                js_content.style.display = 'block';
            } else if (type === 'js') {
                setElementSize(editor_js);
                html_content.style.display = 'block';
                css_content.style.display = 'block';
            }
        }
    }


    var updateSnippet = function (uid, data) {
        var url = site_url + 'snippets/update/' + uid + '/',
            data = {
                title: data.title,
                desc: data.desc,
                html: data.html,
                css: data.css,
                javascript: data.javascript
            }
        axios.post(url, data)
            .then(function (response) {
                console.log(response);
                if (response.data.status) {
                    console.log('Success to update');
                    document.getElementById('iframe').contentWindow.location.reload();
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }


    var html_btn = document.querySelector('.html-section .zoom'),
        css_btn = document.querySelector('.css-section .zoom'),
        js_btn = document.querySelector('.js-section .zoom'),
        html_content = document.querySelector('.html-section'),
        css_content = document.querySelector('.css-section'),
        js_content = document.querySelector('.js-section'),
        mtitle = document.querySelector('#mtitle'),
        mdesc = document.querySelector('#mdesc'),
        updateData = document.querySelector('.updateData'),
        updateModal = document.querySelector('.updateModal');

    var updateDataFn = function(e){
        e.preventDefault();
        var uid = this.getAttribute('data-uid');
        var data = {
            title: mtitle.value,
            desc: mdesc.value,
            html: editor_html.getValue(),
            css: editor_css.getValue(),
            javascript: editor_js.getValue()
        }
        console.log(data);
        updateSnippet(uid, data);
    }
    updateData.addEventListener('click', updateDataFn);
    updateModal.addEventListener('click', updateDataFn);

    document.addEventListener("keydown", function (event) {
        if (event.ctrlKey && event.keyCode === 13) {
            var uid = updateData.getAttribute('data-uid');
            var data = {
                title: mtitle.value,
                desc: mdesc.value,
                html: editor_html.getValue(),
                css: editor_css.getValue(),
                javascript: editor_js.getValue()
            }
            console.log(data);
            updateSnippet(uid, data);
        }
    });



    // Set size
    setElementSize(editor_html);
    setElementSize(editor_css);
    setElementSize(editor_js);


    //Split editor
    Split(['.left-content', '.right-content'], {
        sizes: [40, 60],
        minSize: 200,
        gutterSize: 8,
        cursor: 'row-resize'
    });

    // toggle full screen
    html_btn.addEventListener('click', function (e) {
        e.preventDefault();
        toogleSize(html_btn, 'html');
    });
    css_btn.addEventListener('click', function (e) {
        e.preventDefault();
        toogleSize(css_btn, 'css');
    });
    js_btn.addEventListener('click', function (e) {
        e.preventDefault();
        toogleSize(js_btn, 'js');
    });

    // on resize
    window.addEventListener('resize', function (e) {
        setElementSize(editor_html);
        setElementSize(editor_css);
        setElementSize(editor_js);
    });






}

// remove notification 3s
if (document.querySelector('.notification')){
    var w = setTimeout(function(){
        document.querySelector('.notification').remove();
        clearTimeout(w);
    },3000);
}
