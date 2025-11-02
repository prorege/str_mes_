<template>
    <div v-if="vars.init">
        <div class="buttons">
            <button type="button" class="print-button" @click="methods.printReport">인쇄</button>
            <button type="button" class="edit-button" @click="methods.editReport">{{ vars.formState.readOnly ? '수정' : '취소' }}</button>
            <button type="button" class="save-button" @click="methods.saveReport">저장</button>
        </div>
        <div class="report">
            
            <div class="content-header">
                <div class="content-header-container">
                    <div class="content-header-title" style="text-align: center;">
                        <span style="font-size: 32px; font-weight: bold;">한국자동제어공업협동조합</span>
                    </div>
                </div>
            </div>
            <div class="content-body">
                <div class="content-body-container">
                    <div class="body-1">
                        <div style="text-align: center; margin-bottom: 3px;">서울시 송파구 송이로15길 14 (자동제어조합회관) / T:582-7834 (오영환) / F: 582-7803</div>
                        <div class="underline"></div>
                        <div style="width: 100%; display: flex; padding: 10px 3px;">
                            <div style="width: 50%;">
                                <div style="display: flex;">
                                    <span style="width: 70px; display: flex; justify-content: space-between;">
                                        <span>문</span>
                                        <span>서</span>
                                        <span>번</span>
                                        <span>호</span>
                                    </span>
                                    <span>&nbsp;: 자제(사) 제&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;호</span>
                                </div>
                                <div style="display: flex;">
                                    <span style="width: 70px; display: flex; justify-content: space-between;">
                                        <span>시</span>
                                        <span>행</span>
                                        <span>일</span>
                                        <span>자</span>
                                    </span>
                                    <span>&nbsp;: {{ methods.commencementDate() }}</span>
                                </div>
                                <div style="display: flex;">
                                    <span style="width: 70px; display: flex; justify-content: space-between;">
                                        <span>수</span>
                                        <span>신</span>
                                    </span>
                                    <span>&nbsp;: {{ vars.formData.project_management.contract_company }} </span>
                                </div>
                                <div style="display: flex;">
                                    <span style="width: 70px; display: flex; justify-content: space-between;">
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
                            <span style="width: 70px; display: flex; justify-content: space-between;">
                                <span>제</span>
                                <span>목</span>
                            </span>
                            <span>&nbsp;: {{ vars.formData.project_management.project_name }} 관련 착수계 제출의 건 </span>
                        </div>
                        
                    </div>
                    <div class="body-2" >
                        <div>
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
                        <div>
                            <div>
                                <span>2.&nbsp;</span>
                                <span>우수조달공동상표 물품으로 계약 체결한 "{{ vars.formData.project_management.project_name }}" 건과 관련하여 아래와 같이 착수게 및 관련 서류를 제출합니다.
                                </span>
                            </div>
                            <div style="width: 100%; padding: 10px; display: flex; flex-direction: column; gap: 3px;">
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
                            <div style="width: 100%; display: flex; padding: 0px 3px;"> 
                                <table style="table-layout: fixed; border-collapse: separate; border-spacing: 0 3px;">
                                    <tbody>
                                        <colgroup>
                                            <col style="width: 8%;" />
                                            <col style="width: 92%;" />
                                        </colgroup>
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
                                            <td>5.&nbsp;&nbsp;현잔대리인계 1부</td>
                                        </tr>
                                        <tr>
                                            <td>6.&nbsp;&nbsp;예정공정표 1부 끝.</td>
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
                    <div style="display: flex; justify-content: space-between; font-size: 32px; font-weight: bold;">
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
                    <div style="display: flex; justify-content: space-between; font-size: 32px; font-weight: bold;">
                        <span>이&nbsp;&nbsp;&nbsp;사&nbsp;&nbsp;&nbsp;장</span>
                        <span>최&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;전&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;남</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import html2canvas from 'html2canvas';
import { reactive, onMounted, ref, watch, onUnmounted } from 'vue';
import DxTextBox from 'devextreme-vue/text-box';
import { projectRegistration, projectReport } from '../../data-source/project';

export default {
    components: {
        DxTextBox,
    },
    props: {
        fk_project_management_id: {
            type: Number,
            required: true,
        },
        show: {
            type: Boolean,
            default: false,
        },
    },
    setup(props) {
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
                if (!vars.formData.id) return;
                const item = document.querySelector('.report');
     
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
            }
        }
        watch(
            () => props.show, 
            async () => {
                await methods.initById(props.fk_project_management_id);
        }, { immediate: true });

        return { vars, methods }
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
                border-bottom: 1px dotted #000;

                .underline {
                    width: 100%;
                    height: 17px;
                    background-color: #bbd1f8;
             
                }
            }
            .body-2 {
                padding: 10px 3px 0px 3px;   
               
            }
        }
    }    
    .content-footer {
        margin-top: auto;
        margin-bottom: 50px;

    }
}
</style>