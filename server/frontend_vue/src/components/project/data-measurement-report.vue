<template>
    <div class="report">
        <div class="buttons">
            <button type="button" class="print-button" @click="methods.printReport">인쇄</button>
        </div>
        <div class="content-header">
            <div class="content-header-container">
                <div class="content-header-title" style="text-align: center;">
                    <span style="font-size: 26px; font-weight: 500;">한국계측제어공업협동조합</span>
                </div>
            </div>
        </div>
        <div class="content-body">
            <div class="content-body-container">
                <div class="body-1">
                    <table>
                        <tbody>
                            <colgroup>
                                <col style="width: 55px;" />
                                <col style="width: 100px;" /> 
                                <col style="width: 40px;" />
                                <col style="width: 100px;" />
                                <col style="width: 40px;" />
                                <col style="width: 100px;" />
                                <col style="width: 100px;" />
                            </colgroup>
                            <tr>
                                <td>우편번호</td>
                                <td>: 08590</td>
                                <td>주 소</td>
                                <td colspan="4">: 서울시 금천구 가산디지털2로 14, (대륭테크노타운12차 211호)</td>
                            </tr>
                            <tr>
                                <td>담 당</td>
                                <td>: 박남연 과장</td>
                                <td>전 화</td>
                                <td>: 02-853-2623</td>
                                <td>전 송</td>
                                <td>: 02-853-2624</td>
                                <td style="color: #c56a6a;">kicic7815@daum.net</td>
                            </tr>
                            <tr>
                                <td colspan="7">
                                    <div class="underline"></div>
                                </td>
                            </tr>
                            <tr>
                                <td>문서번호</td>
                                <td colspan="6">: 계제 제&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;호</td>
                            </tr>
                            <tr>
                                <td colspan="7" style="line-height: 10px; padding: 0;">&nbsp;</td>
                            </tr>
                            <tr>
                                <td style="display: flex; justify-content: space-between;">
                                    <span>수</span><span>신</span>
                                </td>
                                <td colspan="6">: 수요기관 </td>
                            </tr>
                            <tr>
                                <td style="display: flex; justify-content: space-between;">
                                    <span>참</span><span>조</span>
                                </td>
                                <td colspan="6">: 텍스트창 </td>
                            </tr>
                            <tr>
                                <td style="display: flex; justify-content: space-between;">
                                    <span>제</span><span>목</span>
                                </td>
                                <td colspan="6">: "프로젝트명" 관련 착수계 제출의 건 </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
           
            </div>
        </div>
    </div>
</template>
<script>
import html2canvas from 'html2canvas';

export default {
    components: {

    },
    props: {
        
    },
    setup(props) {
        const methods = {
            async printReport() {
                const item = document.querySelector('.report');
                const parent = item.parentElement;
                const canvas = await html2canvas(item, { backgroundColor: '#fff', scale: 2 });
                const imgData = canvas.toDataURL('image/png');
                
                const html = `
                <html>
                    <head>
                    <title>인쇄</title>
                    <meta charset="utf-8">
                    <style>
                        @page { 
                            size: A4; 
                            margin: 0; 
                        }
                        * { 
                            margin: 0; 
                            padding: 0; 
                            box-sizing: border-box; 
                        }
                        html, body { 
                            width: 210mm; 
                            height: 297mm; 
                            overflow: hidden; 
                        }
                        img { 
                            width: 210mm; 
                            height: auto; 
                            display: block; 
                        }
                    </style>
                    </head>
                    <body>
                        <img src="${imgData}" />
                    </body>
                </html>
                `;
                const printWindow = window.open('', '_blank', 'width=900,height=1200');

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
                    
            },
        }

        return { methods }
    }
}

</script>

<style lang="scss" scoped>
.report {
    font-family: sans-serif; 
    -webkit-print-color-adjust: exact; 
    width: 210mm; 
    height: 297mm; 
    box-sizing: border-box; 
    padding: 8px;
    font-size: 15px;
    border: 1px dotted #9c9c9c;
    table {width: 100%; border-collapse: collapse;}
    table.fixed { table-layout: fixed; }

    .content-header {
        margin-top: 30px;
        margin-bottom: 25px;
    }
    .content-body {
        width: 80%;
        margin: 0 auto;
        .content-body-container {
            width: 100%;
            .body-1 {
                width: 100%;

                .underline {
                    width: 100%;
                    height: 17px;
                    background-color: #bbd1f8;
             
                }
            }
        }
    }    
}
</style>