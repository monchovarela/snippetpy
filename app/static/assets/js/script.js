// @prepros-append ../lib/axios.min.js

const debug = arr => {
    let json = JSON.stringify(arr, true, 2);
    console.log('========= Debug Javascript ==========');
    console.log(json);
    console.log('=====================================');
}

const get = (selector, scope) => {
    scope = scope ? scope : document;
    return scope.querySelector(selector);
};

const getAll = (selector, scope) => {
    scope = scope ? scope : document;
    return scope.querySelectorAll(selector);
};

const wrapper = get('#wrapper');
if (wrapper) {

    // load window
    const loadWindow = ($mode, $id) => {
        // init codemirror
        const editor = CodeMirror.fromTextArea(get($id), {
            lineNumbers: true,
            lineWrapping: true,
            autofocus: false,
            autoCloseBrackets: true,
            matchBrackets: false,
            tabMode: 'indent',
            mode: $mode,
            theme: 'seti'
        });
        editor.setOption("extraKeys", {
            Tab: function(cm) {
                let spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
                cm.replaceSelection(spaces);
            }
        });
        wrapper.classList.add('loaded');
        return editor;
    }
    // set size
    const setElementSize = (elem, full) => {
        let h = window.innerHeight;
        if (full) elem.setSize(null, h - 25);
        else elem.setSize(null, h / 3 - 32);
    }

    // Modes
    let htmlMode = 'text/html',
        cssMode = 'text/css',
        jsMode = 'text/javascript',
        editor_html = loadWindow(htmlMode, '#html'),
        editor_css = loadWindow(cssMode, '#css'),
        editor_js = loadWindow(jsMode, '#javascript');

    // Toggle full section 
    const toogleSize = (elem, type) => {
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

    // Post data
    const postData = async (url, arr) => {
        const resp = await axios.post(url, arr);
        const result = await resp.data;
        return result;
    }
    // Get data
    const getData = async (url) => {
        const resp = await axios.get(url);
        const result = await resp.data;
        return result;
    }
    // Update snippet
    const updateSnippet = (uid, arr) => {
        let url = site_url + 'snippets/update/' + uid + '/',
            args = {
                title: arr.title,
                desc: arr.desc,
                html: arr.html,
                css: arr.css,
                javascript: arr.javascript
            };

        const update = postData(url, args);
        update.then(res => {
            if (res.status) {
                window.iframe.contentWindow.location.reload();
            }
        });
    }

    let html_btn = get('.html-section .zoom'),
        css_btn = get('.css-section .zoom'),
        js_btn = get('.js-section .zoom'),
        html_content = get('.html-section'),
        css_content = get('.css-section'),
        js_content = get('.js-section'),
        mtitle = get('#mtitle'),
        mdesc = get('#mdesc'),
        updateData = get('.updateData'),
        updateModal = get('.updateModal');

    const updateDataFn = function(event) {
        event.preventDefault();
        let uid = window.iframe.getAttribute('data-uid'),
            args = {
                title: mtitle.value,
                desc: mdesc.value,
                html: editor_html.getValue(),
                css: editor_css.getValue(),
                javascript: editor_js.getValue()
            }
        updateSnippet(uid, args);
    }

    updateData.addEventListener('click', updateDataFn);
    updateModal.addEventListener('click', updateDataFn);
    document.addEventListener("keydown", function(event) {
        if (event.ctrlKey && event.keyCode === 13) {
            updateDataFn(event);
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
    html_btn.addEventListener('click', function(e) {
        e.preventDefault();
        toogleSize(html_btn, 'html');
    });
    css_btn.addEventListener('click', function(e) {
        e.preventDefault();
        toogleSize(css_btn, 'css');
    });
    js_btn.addEventListener('click', function(e) {
        e.preventDefault();
        toogleSize(js_btn, 'js');
    });

    // on resize
    window.addEventListener('resize', function(e) {
        setElementSize(editor_html);
        setElementSize(editor_css);
        setElementSize(editor_js);
    });
}

// remove notification 3s
if (get('.notification')) {
    var w = setTimeout(function() {
        get('.notification').remove();
        clearTimeout(w);
    }, 3000);
}