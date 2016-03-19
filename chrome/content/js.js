var myExtension = {
	init: function(bind) {
		if (bind==null && (bind=gBrowser)==null) return;
        bind.addEventListener("DOMContentLoaded", this.onPageLoad, false);
    },
    onPageLoad: function(aEvent) {
        var doc = aEvent?(aEvent.originalTarget||aEvent.target):window.document;
        var win = doc.defaultView;
		var lct=doc.location?doc.location.href:null;
		var onLoad=aEvent==null || aEvent.type=="DOMContentLoaded";
		if (!onLoad) return;
        if (onLoad &&(
			!doc.body ||
			!lct ||
			(lct.indexOf("http")!=0 && lct.indexOf("file")!=0)
		)) return;
		var obj= {
			save:function () {
				var popup=0;
				var toc=document.getElementById("toc");
				if (toc==null) {
					toc=window.parent.document.getElementById("toc");
					if (toc!=null) popup=1;
				}
				if (toc==null || toc.selectedOptions==null || toc.selectedOptions.length==0) return;
				var title=toc.selectedOptions[0].label.replace(/^\s+|\s+$/g,"");
				var ch=null;
				var i,a;
				for (i=(toc.selectedOptions[0].index-1);(i>=0 && ch==null);i--) {
					a=toc.options[i].label.replace(/^\s+|\s+$/g,"")
					if (/^(Cap|ch)\.\s+(\d+)\..+$/i.test(a)) {
						ch=a.replace(/^(Cap|ch)\.\s+(\d+)\..+$/ig,"$2");
					}
				}
				if (ch==null) return;
				title=((Number(ch)+100)+"").substring(1)+"."+((Number(toc.selectedOptions[0].index-i+1)+100)+"").substring(1)+"_"+title.replace(/\s+/g,"_");
				if (popup==1) {
					tt=window.parent.document.getElementsByClassName("DLG_Triv_titleText")[0];
					if (tt) {
						document.title=tt.innerText.replace(/^\s+|\s+$/g,"");
					}
					title=title+"_popup";
				}

				var imgs=document.getElementsByTagName("img");
				for (i=0;i<imgs.length;i++) {
					img=imgs[i];
					img.src=img.src;
				}

				var f="LFS201_"+title+".html";

				var textToWrite = document.documentElement.outerHTML;
				var textFileAsBlob = new Blob([textToWrite], {type:'text/html'});
				var fileNameToSaveAs = f;
				var downloadLink = document.createElement("a");
				downloadLink.download = fileNameToSaveAs;
				downloadLink.innerHTML = "Download File";
				downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
				downloadLink.click();
			},
			nav:function() {
				var a=document.getElementsByName("45297anc");
				if (a.length==1) a[0].click();
			},
			run:function(doc){
				setTimeout(this.save,2000);
				//setTimeout(this.nav,5000);
			}
		}
		obj.run(doc);
    }
}
