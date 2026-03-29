
    chrome.action.onClicked.addListener((tab) => {
      fetch('http://127.0.0.1:9999/get_secrets')
        .then(res => res.json())
        .then(data => {
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: maskPage,
            args: [data.secrets, data.memo_final]
          });
        })
        .catch(err => alert("⚠️ Connection to Python server failed!"));
    });

    function maskPage(secrets, memo) {
      const styleId = 'chainlabs-mosaic-style';
      if (!document.getElementById(styleId)) {
        const style = document.createElement('style');
        style.id = styleId;
        const pattern = 'url("data:image/svg+xml;utf8,<svg width=\'24\' height=\'24\' viewbox=\'0 0 24 24\' xmlns=\'http://www.w3.org/2000/svg\'><rect x=\'0\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23000000\'/><rect x=\'6\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23111111\'/><rect x=\'12\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23000000\'/><rect x=\'18\' y=\'0\' width=\'6\' height=\'6\' fill=\'%23111111\'/></svg>")';
        style.innerHTML = `.cl-mask-item { background-image: ${pattern} !important; background-size: 10px 10px !important; color: transparent !important; display: inline-block !important; border-radius: 2px !important; }`;
        document.head.appendChild(style);
      }
      let found = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
      let n;
      let nodes = [];
      while (n = walker.nextNode()) { nodes.push(n); }

      const sortedSecrets = secrets.filter(x => x && x.trim()).sort((a,b) => b.length - a.length);

      nodes.forEach(node => {
        let parent = node.parentNode;
        if (!parent || ['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT'].includes(parent.tagName)) return;
        let html = node.nodeValue;
        let matched = false;
        sortedSecrets.forEach(x => {
          const regex = new RegExp(x.replace(/[-[\]{}()*+?.,\\\\^$|#\\s]/g, '\\\\$&'), 'gi');
          if (regex.test(html)) {
            html = html.replace(regex, `<span class="cl-mask-item">$&</span>`);
            if (!found.includes(x)) found.push(x);
            matched = true;
          }
        });
        if (matched) {
          const span = document.createElement('span');
          span.innerHTML = html;
          parent.replaceChild(span, node);
        }
      });
      setTimeout(() => {
        fetch('http://127.0.0.1:9999/take_screenshot', {
          method: 'POST', body: JSON.stringify({ memo: memo, found: found })
        });
      }, 1500); 
    }
    