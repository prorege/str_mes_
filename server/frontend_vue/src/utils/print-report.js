import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf';
import workerSrc from 'pdfjs-dist/legacy/build/pdf.worker.entry';
import html2canvas from 'html2canvas';
pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;

const pdfToImages = async (pdfUrl) => {
    const base = (process.env.BASE_URL || '/').replace(/\/?$/, '/');
    const CMAP_URL = new URL('pdfjs/cmaps/',         location.origin + base).toString();
    const FONT_URL = new URL('pdfjs/standard_fonts/', location.origin + base).toString();
    const loadingTask = pdfjsLib.getDocument({
        url: pdfUrl,
        cMapUrl: CMAP_URL,          
        cMapPacked: true,           
        standardFontDataUrl: FONT_URL,
        useWorkerFetch: true        
    });
    const pdf = await loadingTask.promise;
    const numPages = pdf.numPages;
    const images = [];

    for (let pageNum = 1; pageNum <= numPages; pageNum++) {
        const page = await pdf.getPage(pageNum);
        const viewport = page.getViewport({ scale: 2 });

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        await page.render({ canvasContext: context, viewport }).promise;

        images.push(canvas.toDataURL()); 
    }

    return images; 
};

const printReport = async (documentName, data, _grid, options = {}) => {
    const { landscape = false } = options; 

    let attachmentHtml = '';
 
    if (data.length > 0) {
        for (const item of data) {
            if (documentName.includes(item.document_name)) {
                const ext = item.file_name.split('.').pop().toLowerCase();
                if (ext === 'pdf') {
                    const pdfUrl = `/api/mes/v1/file-manager/read/${item.file_path}/${item.file_name}`;
                    const imgList = await pdfToImages(pdfUrl); 
                    for (const img of imgList) {
                        attachmentHtml += `
                            <div class="print-page" style="page-break-after: always;"><img src="${img}" /></div>
                        `;
                    }
                } else if (['jpg', 'jpeg', 'png'].includes(ext)) {
                    attachmentHtml += `
                        <div class="print-page" style="page-break-after: always;"><img src="/api/mes/v1/file-manager/read/${item.file_path}/${item.file_name}" style="max-width: 100%;" /></div>
                    `;
                }
            }
        }
    }

   
    const items = _grid.querySelectorAll('.report');
    const imgData = [];
    for (const item of items) {
        const canvas = await html2canvas(item, { backgroundColor: '#fff', scale: 2 });
        const img = canvas.toDataURL('image/png');
        imgData.push(img);
    }

    const html = `
    <html>
        <head>
        <title>인쇄</title>
        <meta charset="utf-8">
        <style>
            @page { 
                size: A4 ${landscape ? 'landscape' : 'portrait'};
                margin: 0; 
            }
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }
            html, body { 
                margin: 0; 
                padding: 0; 
            }
            .print-page {
                width: ${landscape ? '297mm' : '210mm'};
                height: ${landscape ? '210mm' : '297mm'};
                page-break-after: always;
                page-break-inside: avoid;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .print-page:last-child {
                page-break-after: auto;
            }
            .print-page img {
                width: ${landscape ? '292mm' : '205mm'};
                height: auto;
                display: block;
            }
        </style>
        </head>
        <body>
            ${imgData.map((img, index) => {
                const isLast = index === imgData.length - 1;
                return `<div class="print-page" style="page-break-after: ${isLast ? 'auto' : 'always'};"><img src="${img}" /></div>`;
            }).join('\n')}
            ${attachmentHtml}
        </body>
    </html>
    `;
    
    let printWindow = window.open('', '_blank', 'width=900,height=1200');

    if (!printWindow) {
  
        const iframe = document.createElement('iframe');
        iframe.style.position = 'fixed';
        iframe.style.right = '0';
        iframe.style.bottom = '0';
        iframe.style.width = '0';
        iframe.style.height = '0';
        iframe.style.border = '0';
        document.body.appendChild(iframe);
        
        const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
        if (!iframeDoc) {
            document.body.removeChild(iframe);
            console.error('인쇄를 위한 iframe을 생성할 수 없습니다.');
            return;
        }
        
        iframeDoc.open();
        iframeDoc.write(html);
        iframeDoc.close();
        
        await (async function waitForAllImages(doc) {
            const imgs = Array.from(doc?.images || []);
            if (!imgs.length) return;
            await Promise.all(imgs.map(img => img.complete ? Promise.resolve() : new Promise(res => {
                img.onload = img.onerror = res;
            })));
        })(iframeDoc);
        
        iframe.contentWindow?.focus();
        iframe.contentWindow?.print();
        
        setTimeout(() => {
            try {
                if (iframe.parentNode) {
                    document.body.removeChild(iframe);
                }
            } catch (e) {
                console.warn('iframe 제거 실패:', e);
            }
        }, 1000);
        return;
    }

    try {
        printWindow.document.write(html);
        printWindow.document.close();
        await (async function waitForAllImages(doc) {
            const imgs = Array.from(doc?.images || []);
            if (!imgs.length) return;
            await Promise.all(imgs.map(img => img.complete ? Promise.resolve() : new Promise(res => {
                img.onload = img.onerror = res;
            })));
        })(printWindow.document);
        printWindow.focus();
        printWindow.print();
    } catch (error) {
        console.error('인쇄 중 오류 발생:', error);
        printWindow.close();
    }
};


export { printReport };