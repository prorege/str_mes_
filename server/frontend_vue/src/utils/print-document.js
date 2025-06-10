import { template, templateSettings } from 'lodash'
import html2canvas from 'html2canvas' 
import { jsPDF } from 'jspdf'
import numeral from 'numeral'
import moment from 'moment'
import ApiService from './api-service'
import authService from '../auth';
import {businessNumberFormat} from './util'

const apiService = new ApiService('/api/mes/v1/common/companies');
const _host = location.origin
let _company = null

templateSettings.imports.moment = moment
templateSettings.imports.numeral = numeral
        
const documentWrapper = (body, title='문서출력', exportToImg=false) => {
  let script = '<button type="button" class="print-button" onclick="window.print()">인쇄</button>'

  if (exportToImg) {
    script = ''
  }

  return `
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>${title}</title>
      <style>
        body { font-family: sans-serif; -webkit-print-color-adjust: exact; }
        .print-document {position: relative;}
        table {width: 100%; border-collapse: collapse;}
        table.fixed { table-layout: fixed; }
        th, td { padding-top: 4px; padding-bottom: 3px; font-size: 12px; }
        th { padding-left: 8px; padding-right: 8px; text-align: justify; text-align-last: justify; white-space: nowrap; }
        td { padding-left: 8px; padding-right: 8px; }
        table.lined-all th,
        table.lined-all td { border: 1px solid #000; }
        table.lined-outer { border: 1px solid #000; } 
        .title {font-size: 24px; max-width: 240px; margin: 20px auto;}
        .subtitle {font-size: 21px;}
        .align-left { text-align: left; }
        .align-center { text-align: center; }
        .align-right { text-align: right; text-align-last: auto; }
        .print-button {
          border: 1px solid #b1b1b1;
          border-radius: 8px;
          padding: 0 20px;
          height: 30px;
          position: fixed;
          top: 10px;
          left: 10px;
          background-color: #d8d8d8;
          color: #414141;
          box-shadow: 0px 1px 1px rgb(0 0 0 / 20%);
          z-index: 10;
        }
        .text-ellipsis { overflow: hidden; text-overflow: ellipsis; }

        @media print {
          .print-button { display: none; }
        }
      </style>
    </head>
    <body>
      ${body}
      ${script}
    </body>
    </html>
  `
}

export async function printDocument (type, params) {
  try {
    const t = (await import(`./templates/${type}.js`)).default
    if (!_company) {
      const {data: company} = await apiService.get(String(authService.getCompanyId()))
      company.business_number = businessNumberFormat(company.business_number)
      _company = company
    }
    const body = template(t)({...params, _company, _host})
    const w = window.open('', 'print-document', 'width=800,height=800')
    w.document.body.innerHTML = documentWrapper(body, _company.name)
  }
  catch (ex) {
    console.error(ex)
    return null
  }
}

export async function saveDocumentToBlob (type, params) {
  let w = null
  try {
    const t = (await import(`./templates/${type}.js`)).default
    if (!_company) {
      const {data: company} = await apiService.get(String(authService.getCompanyId()))
      company.business_number = businessNumberFormat(company.business_number)
      _company = company
    }
    const body = template(t)({...params, _company, _host})
    // w = window.open('', 'print-document', 'width=800,height=800')
    // w.document.body.innerHTML = documentWrapper(body, _company.name, true)

    // const cv = await html2canvas(w.document.body, {
    //   windowWidth: 800,
    //   windowHeight: 800
    // })
    // const img = cv.toDataURL('image/jpeg', 1)
    // const doc = new jsPDF({ format: 'a4', unit: 'mm' })
    // doc.addImage(img, 'JPEG', 0, 0, 210, 210, null, 'NONE')
    // const blob = doc.output('blob', {filename: `${Date.now()}.pdf`})
    // w.close()
    const ctx = documentWrapper(body, _company.name, true)
    const blob = new Blob([ctx], { type: 'text/html' })
    return blob
  }
  catch (ex) {
    console.error(ex)
    if (w && !w.closed) w.close()
    return null
  }
}

export async function saveDocumentToPdfBlob (type, params){
  let w = null
  try {
    const t = (await import(`./templates/${type}.js`)).default
    if (!_company) {
      const {data: company} = await apiService.get(String(authService.getCompanyId()))
      company.business_number = businessNumberFormat(company.business_number)
      _company = company
    }
    
    const body = template(t)({...params, _company, _host});

    const container = document.createElement('div');
    container.innerHTML = documentWrapper(body, _company.name);
    container.style.overflow = 'hidden';
    container.style.position = 'absolute';
    container.style.top = '-9999px';  

    const bottomElement = container.querySelector('.bottom');
    const printDocument = container.querySelector('.print-document');
    if(printDocument){
      printDocument.style.margin = '20px';
      printDocument.style.fontWeight = 600;
    }
    if (bottomElement) {
      bottomElement.remove();
    }
    document.body.appendChild(container);

    const canvas = await html2canvas(container, { scale: 3 })

    
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    
    const imgProps = pdf.getImageProperties(imgData)
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)

    const pdfBlob = pdf.output('blob')
    document.body.removeChild(container);
    return pdfBlob
  }
  catch (ex) {
    console.error(ex)
    return null
  }
}

export default printDocument