<template>
     <dx-popup
      :visible="props.visible"
      content-template="popup-content"
      title="자동제어조합 착수계"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @update:visible="(value) => emit('update:visible', value)"
      width="230mm"
      height="700px"
    >
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :options="{ 
                text: '인쇄',
                icon: 'print', 
                onClick: methods.printReport 
            }"/>
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :options="{ 
                text: vars.formState.readOnly ? '수정' : '취소',
                icon: 'edit', 
                onClick: methods.editReport 
            }"/>
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :options="{ 
                text: '저장',
                icon: 'save', 
                onClick: methods.saveReport 
            }"/>
        <template #popup-content>
            <dx-scroll-view width="100%" height="100%">

                <div v-if="vars.init" class="auto-commencement-report">
                    <div class="report-container">
                        <div class="report">
                            <div class="content-header">
                                <div class="content-header-container">
                                    <div class="content-header-title" style="text-align: center;">
                                        <span style="font-size: 32px; font-weight: 400;">한국자동제어공업협동조합</span>
                                    </div>
                                </div>
                            </div>
                            <div class="content-body">
                                <div class="content-body-container">    
                                    <div class="body-1">
                                        <div style="text-align: center; margin-bottom: 3px;">서울시 송파구 송이로15길 14 (자동제어조합회관) / T:582-7834 (오영환) / F: 582-7803</div>
                                        <div class="underline"></div>
                                        <div style="width: 100%; display: flex; padding: 10px 3px;">
                                            <div style="width: 50%; display: flex; flex-direction: column; gap: 10px;">
                                                <div style="display: flex;">
                                                    <span style="width: 70px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>문</span>
                                                        <span>서</span>
                                                        <span>번</span>
                                                        <span>호</span>
                                                    </span>
                                                    <span>&nbsp;: 자제(사) 제&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;호</span>
                                                </div>
                                                <div style="display: flex;">
                                                    <span style="width: 70px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>시</span>
                                                        <span>행</span>
                                                        <span>일</span>
                                                        <span>자</span>
                                                    </span>
                                                    <span>&nbsp;: {{ methods.commencementDate() }}</span>
                                                </div>
                                                <div style="display: flex;">
                                                    <span style="width: 70px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>수</span>
                                                        <span>신</span>
                                                    </span>
                                                    <span>&nbsp;: {{ vars.formData.project_management.contract_company }} </span>
                                                </div>
                                                <div style="display: flex;">
                                                    <span style="width: 70px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>참</span>
                                                        <span>조</span>
                                                    </span>
                                                    <span v-if="!vars.formState.readOnly">&nbsp;: <input type="text" v-model="vars.formData.attr01"> </span>
                                                    <span v-else>&nbsp;: {{ vars.formData.attr01 }} </span>
                                                </div>
                                            </div>
                                            <div style="width: 50%;">
                                                <table border="1">
                                                    <tbody>
                                                        <tr>
                                                            <td style="text-align: center;">취급</td>
                                                            <td colspan="3"></td>
                                                            <td colspan="4" style="text-align: center;"> 이 사 장 </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="text-align: center;">보존</td>
                                                            <td colspan="2" style="border-right: none;"></td>
                                                            <td style="border-left: none;">년</td>
                                                            <td colspan="4" style="text-align: center; border-bottom: none;"></td>
                                                        </tr>
                                                        <tr>
                                                            <td colspan="2" rowspan="2" style="text-align: center;">전무이사</td>
                                                            <td style="text-align: center;">전결</td>
                                                            <td rowspan="2" style="border-left: none;"></td>
                                                            <td colspan="4" rowspan="2" style="text-align: center; border-top: none;"></td>
                                                        </tr>
                                                        <tr>
                                                            <td style="text-align: center; border-right: none;">&nbsp;</td>
                                                        </tr>
                                                        <tr height="40px;">
                                                            <td colspan="2" style="text-align: center;">이사</td>
                                                            <td colspan="2" style="text-align: center;">한관수</td>
                                                            <td colspan="4" style="border-bottom: none;"></td>
                                                        </tr>
                                                        <tr height="40px;">
                                                            <td colspan="2" style="text-align: center;">기안</td>
                                                            <td colspan="2" style="text-align: center;">오영한</td>
                                                            <td colspan="2" style="border-top: none;"></td>
                                                            <td colspan="2" style="text-align: center;">협조</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                        <div style="display: flex; padding: 0px 3px;">    
                                            <span style="width: 70px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                <span>제</span>
                                                <span>목</span>
                                            </span>
                                            <span>&nbsp;: {{ vars.formData.project_management.project_name }} 관련 착수계 제출의 건 </span>
                                        </div>
                                        
                                    </div>
                                    <div class="body-2" >
                                        <div style="margin-bottom: 10px;">
                                            <div>
                                                <span>1. 귀&nbsp;</span>
                                                <span v-if="!vars.formState.readOnly">
                                                    <input type="text" v-model="vars.formData.attr02"> 무궁한 발전을 기원합니다.
                                                </span>
                                                <span v-else>
                                                    {{ vars.formData.attr02 }} 무궁한 발전을 기원합니다.
                                                </span>
                                            </div>
                                            
                                        </div>
                                        <div style="margin-bottom: 10px;">
                                            <div>
                                                <span>2.&nbsp;</span>
                                                <span>우수조달공동상표 물품으로 계약 체결한 "{{ vars.formData.project_management.project_name }}" 건과 관련하여 아래와 같이 납품완료계 및 관련 서류를 제출합니다.
                                                </span>
                                            </div>
                                            <div style="width: 100%; padding: 10px; display: flex; flex-direction: column; gap: 8px;">
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">가.</div>
                                                    <div style="width: 90px;">계약 건명 </div>
                                                    <div>:&nbsp;{{ vars.formData.project_management.project_name }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">나.</div>
                                                    <div style="width: 90px;">계약 번호 </div>
                                                    <div v-if="!vars.formState.readOnly">: &nbsp;<input type="text" v-model="vars.formData.attr04"> (구매번호 : <input type="text" v-model="vars.formData.attr05">)</div>
                                                    <div v-else>:&nbsp;{{ vars.formData.attr04 }} (구매번호 : {{ vars.formData.attr05 }})</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">다.</div>
                                                    <div style="width: 90px;">계약년월일 </div>
                                                    <div>:&nbsp;{{ methods.contractData() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">라.</div>
                                                    <div style="width: 90px;">착수년월일 </div>
                                                    <div>:&nbsp;{{ methods.commencementDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">마.</div>
                                                    <div style="width: 90px;">납품 기한 </div>
                                                    <div>:&nbsp;{{ methods.completionDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">바.</div>
                                                    <div style="width: 90px;">계약 금액 </div>
                                                    <div>:&nbsp;一金 {{ methods.companyAmountStr() }}정 (₩ {{ methods.companyAmount() }} VAT 포함)</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">사.</div>
                                                    <div style="width: 200px;">배정업체 세부사항&nbsp;</div>
                                                </div>
                                                <div style="width: 100%; display: flex; padding: 10px 0px;">
                                                    <table border="1">
                                                        <tbody>
                                                            <colgroup>
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                            </colgroup>
                                                            <tr>
                                                                <th>업 체 명</th>
                                                                <td style="text-align: center;">에스텍아이앤씨(주)</td>
                                                                <th>대 표 자</th>
                                                                <td style="text-align: center;">박 길 현</td>
                                                            </tr>
                                                            <tr>
                                                                <th>주소</th>
                                                                <td colspan="3" style="text-align: center;">대전광역시 유성구 문지로 272-37 (2층)</td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                            <div style="width: 100%; display: flex; padding: 10px;"> 
                                                <table style="table-layout: fixed; border-collapse: separate; border-spacing: 0 8px;">
                                                    <colgroup>
                                                        <col style="width: 8%;" />
                                                        <col style="width: 92%;" />
                                                    </colgroup>
                                                    <tbody>
                                                        <tr>
                                                            <td rowspan="6" style="vertical-align: top;">첨부</td>
                                                            <td>1.&nbsp;&nbsp;착수계 1부 </td>
                                                        </tr>
                                                        <tr>
                                                            <td>2.&nbsp;&nbsp;계약서 및 계약내역서 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>3.&nbsp;&nbsp;배정업체 등록서류 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>4.&nbsp;&nbsp;고용산재가입증명원 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>5.&nbsp;&nbsp;현장대리인계 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>6.&nbsp;&nbsp;예정공정표 1부. 끝.</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="content-footer">
                                <div style="text-align: center; width: 55%; margin: 0 auto;">
                                    <div style="display: flex; justify-content: space-between; font-size: 32px; font-weight: 400;">
                                        <span>한</span>
                                        <span>국</span>
                                        <span>자</span>
                                        <span>동</span>
                                        <span>한</span>
                                        <span>제</span>
                                        <span>어</span>
                                        <span>공</span>
                                        <span>업</span>
                                        <span>협</span>
                                        <span>동</span>
                                        <span>조</span>
                                        <span>합</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; font-size: 32px; font-weight: 400;">
                                        <span>이&nbsp;&nbsp;&nbsp;사&nbsp;&nbsp;&nbsp;장</span>
                                        <span>최&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;전&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;남</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="report" style="font-size: 17px; font-weight: 500;">
                            
                            <div class="content-header" style="margin-top: 50px; margin-bottom: 50px;">
                                <div class="content-header-container" style="display: flex; justify-content: space-around; align-items: center;">
                                    <div style="width: 110px;"></div>
                                    <div class="content-header-title" style="text-align: center;">
                                        <span style="font-size: 32px; font-weight: 400; border-bottom: 2px solid #000; padding-bottom: 5px; display: inline-block;">&nbsp;착&nbsp;&nbsp;&nbsp;&nbsp;수&nbsp;&nbsp;&nbsp;&nbsp;계&nbsp;</span>
                                    </div>
                                    <div>
                                        <table border="1" style="width: 110px;">
                                            <tbody>
                                                <tr>
                                                    <th>경유</th>
                                                </tr>
                                                <tr>
                                                    <th height="60px">&nbsp;</th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="content-body">
                                <div class="content-body-container">
                                    <div class="body-2">
                                        <div>
                                            <div style="width: 100%; display: flex; flex-direction: column; gap: 10px;">
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">◉</div>
                                                    <div style="width: 150px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>계</span>
                                                        <span>약</span>
                                                        <span>명</span>
                                                        <span>:</span>
                                                    
                                                    </div>
                                                    <div>{{ vars.formData.project_management.project_name }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">◉</div>
                                                    <div style="width: 150px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>계</span>
                                                        <span>약</span>
                                                        <span>금</span>
                                                        <span>액</span>
                                                        <span>:</span>
                                                    </div>
                                                    <div>一金 {{ methods.companyAmountStr() }}정 (₩ {{ methods.companyAmount() }} VAT 포함)</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">◉</div>
                                                    <div style="width: 150px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>계</span>
                                                        <span>약</span>
                                                        <span>년</span>
                                                        <span>월</span>
                                                        <span>일</span>
                                                        <span>:</span>
                                                    </div>
                                                    <div>{{ methods.contractData() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">◉</div>
                                                    <div style="width: 150px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>착</span>
                                                        <span>수</span>
                                                        <span>년</span>
                                                        <span>월</span>
                                                        <span>일</span>
                                                        <span>:</span>
                                                    </div>
                                                    <div>{{ methods.commencementDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">◉</div>
                                                    <div style="width: 150px; display: flex; justify-content: space-between; margin-right: 10px;">
                                                        <span>납</span>
                                                        <span>품</span>
                                                        <span>기</span>
                                                        <span>한</span>
                                                        <span>:</span>
                                                    </div>
                                                    <div>{{ methods.completionDate() }}</div>
                                                </div>
                                            </div>
                                            
                                        </div>
                                    </div>
                                    <div style="width: 100%; margin-top: 90px; margin-bottom: 90px; text-align: center;">
                                        <div>
                                            위와 같이 착수하였기에 착수계를 제출합니다.
                                        </div>
                                    </div>
                                    <div style="width: 100%; margin-top: 90px; margin-bottom: 90px; text-align: center;">
                                        <div>
                                            {{ methods.commencementDate() }}
                                        </div>
                                    </div>
                                    <div style="width: 100%; margin-top: 90px; margin-bottom: 90px; text-align: right; display: flex; flex-direction: column; gap: 10px;">
                                        <div>
                                            서울시 송파구 송이로 15길 14
                                        </div>
                                        <div>
                                            한국자동제어공업협동조합
                                        </div>
                                        <div style="align-self: flex-end; display: flex; justify-content: space-between; width: 35%">
                                            <span style="">이</span>
                                            <span style="">시</span>    
                                            <span style="">장</span>
                                            <span style="">&nbsp;</span>
                                            <span style="">최</span>
                                            <span style="">전</span>
                                            <span style="">남</span>
                                            <span style="">(인)</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="content-footer">
                                <div style="text-align: center;">
                                    <span style="font-weight: 400; font-size: 32px;">{{ vars.formData.project_management.contract_company }} 귀중 </span>
                                </div>
                            </div>
                        </div>
                    
                    </div>
                </div>
            </dx-scroll-view>
        </template>
    </dx-popup>
</template>
<script>
import html2canvas from 'html2canvas';
import { reactive, onMounted, ref, watch, onUnmounted } from 'vue';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxTextBox from 'devextreme-vue/text-box';
import { projectRegistration, projectReport } from '../../data-source/project';
import { alert } from 'devextreme/ui/dialog';

export default {
    components: {
        DxTextBox,
        DxScrollView,
        DxPopup,
        DxToolbarItem,
    },
    emits: ['update:visible'],
    props: {
        fk_project_management_id: {
            type: Number,
            default: null,
        },
        visible: {
            type: Boolean,
            default: false,
        },
    },
    setup(props, { emit }) {
        const vars = {};
        vars.init = ref(false);
        vars.formState = reactive({
            readOnly: true,
        });
        vars.formData = reactive({
            project_management: reactive({
                contract_company: '', // 수요기관 (수신)
                project_name: '',     // 프로젝트명
                company_amount: 0, // 계약금액
                contract_date: '',              // 계약일자
                commencement_date: '',           // 착공일자 (착수일자)
                completion_date: '',             // 준공일자 (납품일자)
            }),
            fk_project_management_id: null,
            attr01 : '참조',                   // 참조
            
            attr02 : '텍스트입력창 1',      // 텍스트입력창 1
            attr03 : '텍스트입력창 2',      // 텍스트입력창 2
            attr04 : '계약번호',           // 계약번호
            attr05 : '구매번호',           // 구매번호
    
        });
        vars.oldFormData = reactive({});

        const methods = {
            async initById(fk_project_management_id) {
                methods.resetFormData();
                let { data: reportData} = await projectReport.load({ filter: [['fk_project_management_id', '=', fk_project_management_id]] });
                if (reportData.length > 0) {
                    Object.assign(vars.formData, reportData[0]);
                    vars.formState.readOnly = true;
                } else {
                    let { data } = await projectRegistration.byKey(fk_project_management_id);
                    Object.assign(vars.formData.project_management, data);
                    vars.formData.fk_project_management_id = fk_project_management_id;
                    Object.assign(vars.oldFormData, vars.formData);
                    vars.formState.readOnly = false;
                }

                vars.init.value = true;
            },
            resetFormData() {
                Object.assign(vars.formData, {
                    project_management: reactive({}),
                    attr01: '',
                    attr02: '',
                    attr03: '',
                    attr04: '',
                    attr05: '',
                    fk_project_management_id: null, // 
                });
                vars.oldFormData = reactive({});
            },
            async printReport() {
                if (!vars.formData.id) {
                    alert('등록된 데이터가 없습니다. 먼저 데이터를 등록해주세요.', '인쇄');
                    return;
                }
                const grid = document.querySelector('.auto-commencement-report');
                const items = grid.querySelectorAll('.report');
                const imgData = [];
                for (const item of items) {
                    const canvas = await html2canvas(item, { backgroundColor: '#fff', scale: 2 });
                    const img = canvas.toDataURL('image/png');
                    imgData.push(img);
                }
                
                // const imgData = canvas.toDataURL('image/png');
                
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
                            margin: 0; 
                            padding: 0; 
                        }
                        .print-page {
                            width: 210mm;
                            height: 297mm;
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
                            width: 210mm;
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
            editReport() {
                if (vars.formState.readOnly) {
                    Object.assign(vars.oldFormData, vars.formData);
                    vars.formState.readOnly = false;
                } else {
                    Object.assign(vars.formData, vars.oldFormData);
                    vars.formState.readOnly = true;
                }
            },
            async saveReport() {
                if (vars.formState.readOnly) {
                    return;
                }
                if (vars.formData.id) {
                    const updateData = Object.assign({}, vars.formData);
                    delete updateData.id;
                    delete updateData.created;
                    delete updateData.project_management;
                    await projectReport.update(vars.formData.id, updateData);
             
                } else {
                    const insertData = Object.assign({}, vars.formData);
                    delete insertData.id;
                    delete insertData.created;
                    delete insertData.project_management;
                    
                    const { data } = await projectReport.insert(insertData);
                    vars.formData.id = data.id;
                    vars.formData.project_management = data.project_management;
            
                }
                vars.oldFormData = reactive({});
                vars.formState.readOnly = true;
            },
            formatDate(dateStr) {
                if (!dateStr) return '';
                const dateOnly = dateStr.split('T')[0].split(' ')[0];
                return dateOnly.replace(/(\d{4})-(\d{2})-(\d{2})/, '$1년 $2월 $3일');
            },
            contractData() {
                return methods.formatDate(vars.formData.project_management.contract_date);
            },
            commencementDate() {
                return methods.formatDate(vars.formData.project_management.commencement_date);
            },
            completionDate() {
                return methods.formatDate(vars.formData.project_management.completion_date);
            },
            numberToKorean(num) {
                const units = ['', '만', '억', '조', '경'];
                const smallUnits = ['', '십', '백', '천'];
                const numbers = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구'];
                
                if (num === 0) return '영원';
                
                let segments = [];
                let temp = num;
                let unitIndex = 0;
                
                while (temp > 0) {
                    const segment = temp % 10000;
                    if (segment > 0) {
                        let segmentStr = '';
                        let seg = segment;
                        let smallUnitIndex = 0;
                        
                        while (seg > 0) {
                            const digit = seg % 10;
                            if (digit > 0) {
                                if (digit === 1 && smallUnitIndex > 0) {
                                    segmentStr = smallUnits[smallUnitIndex] + segmentStr;
                                } else {
                                    segmentStr = numbers[digit] + smallUnits[smallUnitIndex] + segmentStr;
                                }
                            }
                            seg = Math.floor(seg / 10);
                            smallUnitIndex++;
                        }
                        
                        if (unitIndex > 0) {
                            segmentStr += units[unitIndex];
                        }
                        
                        segments.unshift(segmentStr);
                    }
                    
                    temp = Math.floor(temp / 10000);
                    unitIndex++;
                }
                
                return segments.join('') + '원';
            },
            companyAmountStr() {
                const amount = vars.formData.project_management?.company_amount || 0;
                
                let numAmount = typeof amount === 'string' 
                    ? parseFloat(amount.replace(/,/g, '')) || 0
                    : amount || 0;
                
                const result = Math.floor(numAmount * 1.1);
                
                return methods.numberToKorean(result);
            },
            companyAmount() {
                const amount = vars.formData.project_management?.company_amount ||  0;
                
                let numAmount = typeof amount === 'string' 
                    ? parseFloat(amount.replace(/,/g, '')) || 0
                    : amount || 0;
                
                const result = Math.floor(numAmount * 1.1);
                
                return result.toLocaleString('ko-KR');
            },
            getCurrentDateYYMMDD() {
                const now = new Date();
                const year = now.getFullYear().toString().slice(-2); // 뒤 2자리만
                const month = (now.getMonth() + 1).toString().padStart(2, '0'); // 1월이 0이므로 +1
                const day = now.getDate().toString().padStart(2, '0');
                return year + month + day; // yymmdd 형식
            }
        }
        watch(
            () => props.visible, 
            async () => {
                if (!props.visible) {
                    emit('update:visible', false);
                    return;
                }
                await methods.initById(props.fk_project_management_id);
        }, { immediate: true });

        return { vars, methods, emit, props }
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
    font-size: 16px;
    border: 1px dotted #9c9c9c;
    table {width: 100%; border-collapse: collapse; table-layout: fixed;}
    table.fixed { table-layout: fixed; }

    display: flex;
    flex-direction: column;



    .content-header {
        margin-top: 30px;
        margin-bottom: 25px;
    }
    .content-body {
        width: 85%;
        margin: 0 auto;
        .content-body-container {
            width: 100%;
            .body-1 {
                width: 100%;
                padding-bottom: 10px;
                border-bottom: 1px solid #000;

                .underline {
                    width: 100%;
                    height: 17px;
                    background-color: #bbd1f8;
             
                }
            }
            .body-2 {
                padding-top: 10px;          
            }
        }
    }    
    .content-footer {
        
        margin-top: auto;
        margin-bottom: 50px;
        .underline {
            width: 85%;
            height: 17px;
            background-color: #ebebeb;
        
        }

    }
}
</style>