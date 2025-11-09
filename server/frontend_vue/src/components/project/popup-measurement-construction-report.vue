<template>
     <dx-popup
      :visible="props.visible"
      content-template="popup-content"
      title="계측제어조합 착수계"
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
                <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
                <div v-if="vars.init" class="measurement-construction-report">
                    <div class="report-container">
                
                        <div class="report">
                            
                            <div class="content-header">
                                <img src="../../assets/stech.png" alt="logo" style="width: 150px;">
                                <div class="content-header-container">
                                    <div class="content-header-title" style="text-align: center; display: flex; flex-direction: column; gap: 10px;">
                            
                                        <span>ICT와 제어기술의 융합! 자동화기술을 선도하는 기업!</span>
                                        <span style="font-size: 28px; font-weight: 400;">에스텍아이앤씨주식회사</span>
                                    </div>
                                </div>
                            </div>
                            <div class="content-body">
                                <div class="content-body-container">
                                    <div class="body-1" style="border-bottom: 2px solid #000;">
                                        <div>
                                            <div style="height: 5px;"></div>
                                            <div style="display: flex;">
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>수</span>
                                                    <span>신</span>
                                                </span>
                                                <span>&nbsp;: 한국계측제어공업협동조합 </span>
                                            </div>
                                            <div style="display: flex;">
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>참</span>
                                                    <span>조</span>
                                                </span>
                                                <span>&nbsp;: </span>
                                                <!-- <span v-if="!vars.formState.readOnly">&nbsp;: <input type="text" v-model="vars.formData.attr01"> </span>
                                                <span v-else>&nbsp;: {{ vars.formData.attr01 }} </span> -->
                                            </div>
                                            <div style="display: flex;">
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>경</span>
                                                    <span>유</span>
                                                </span>
                                                <span>&nbsp;: </span>
                                            
                                            </div>
                                            <div style="display: flex;">    
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>제</span>
                                                    <span>목</span>
                                                </span>
                                                <span>&nbsp;: {{ vars.formData.project_management.project_name }} 관련 착수계 제출 </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="body-2">
                                        <div style="margin-bottom: 10px;">
                                            <div>
                                                <span>1. 귀 조합의 무궁한 발전을 기원합니다.
                                                </span>
                                            </div>
                                            
                                        </div>
                                        <div>
                                            <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px;">
                                                <div>2. 우수조달공동상표 물품으로 계약 체곌한 
                                                </div>
                                                <div style="margin-left: 10px;">
                                                    "{{ vars.formData.project_management.project_name }}" 
                                                </div>
                                                <div style="margin-left: 10px;">
                                                    건과 관련하여 아래와 같이 착수계 서류를 제출드립니다.
                                                </div>
                                            </div>
                                            <div style="width: 100%; padding: 10px; display: flex; flex-direction: column; gap: 3px;">
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">가.</div>
                                                    <div style="width: 90px;">계 약 명 :&nbsp;</div>
                                                    <div>{{ vars.formData.project_management.project_name }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">나.</div>
                                                    <div style="width: 90px;">계약금액 :&nbsp;</div>
                                                    <div>一金 {{ methods.companyAmountStr() }}정 (₩ {{ methods.companyAmount() }} VAT 포함)</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">다.</div>
                                                    <div style="width: 90px;">계약일자 :&nbsp;</div>
                                                    <div>{{ methods.contractData() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">라.</div>
                                                    <div style="width: 90px;">착수일자 :&nbsp;</div>
                                                    <div>{{ methods.commencementDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">마.</div>
                                                    <div style="width: 90px;">납품일자 :&nbsp;</div>
                                                    <div>{{ methods.completionDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">바.</div>
                                                    <div style="width: 200px;">배정업체 세부사항&nbsp;</div>
                                                </div>
                                                <div style="width: 100%; display: flex; padding: 10px 30px;">
                                                    <table style="border: 1px solid #000; border-collapse: collapse; width: 100%;">
                                                        <colgroup>
                                                            <col style="width: 25%;" />
                                                            <col style="width: 25%;" />
                                                            <col style="width: 25%;" />
                                                            <col style="width: 25%;" />
                                                        </colgroup>
                                                        <tbody>
                                                            <tr>
                                                                <td style="text-align: center; border: 1px solid #000;">업 체 명</td>
                                                                <td style="text-align: center; border: 1px solid #000;">에스텍아이앤씨(주)</td>
                                                                <td style="text-align: center; border: 1px solid #000;">대 표 자</td>
                                                                <td style="text-align: center; border: 1px solid #000;">박 길 현</td>
                                                            </tr>
                                                            <tr>
                                                                <td style="text-align: center; border: 1px solid #000;">주소</td>
                                                                <td colspan="3" style="text-align: center; border: 1px solid #000;">대전광역시 유성구 문지로 272-37 (2층)</td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                                
                                            </div>
                                            <div style="width: 100%; display: flex; padding: 10px;"> 
                                                <table style="table-layout: fixed; border-collapse: separate; border-spacing: 0 3px;">
                                                    <colgroup>
                                                        <col style="width: 8%;" />
                                                        <col style="width: 92%;" />
                                                    </colgroup>
                                                    <tbody>
                                                        <tr>
                                                            <td rowspan="2" style="vertical-align: top;">첨부 : </td>
                                                            <td>1.&nbsp;&nbsp;착수계 공문 </td>
                                                        </tr>
                                                        <tr>
                                                            <td>2.&nbsp;&nbsp;착수계</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="content-footer" style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                                <div style="text-align: center; margin-bottom: 20px;">
                                    <span style="font-weight: bold; font-size: 22px;">에스텍아이앤씨(주) 대표이사 박 길 현 (인)</span>
                                </div>
                                <div class="underline"></div>
                                <div style="display: flex; flex-direction: column; width: 85%;">
                                    <div style="display: flex;">
                                        <div style="width: 70px">담당</div>
                                        <div>{{ vars.formData.project_management.project_manager }}</div>
                                    </div>
                                    <div style="display: flex;">
                                        <div style="width: 70px">협조자</div>
                                        <div></div>
                                    </div>
                                    <div style="display: flex; width: 100%;">
                                        <div style="width: 70px">시 행</div>
                                        <div style="width: 130px;">ST+{{ methods.getCurrentDateYYMMDD() }}+01</div>
                                        <div style="width: 170px;">(에스텍아이앤씨(주)</div>
                                        <div style="width: 170px;">접 수</div>
                                        <div style="width: 90px;">(</div>
                                        <div style="width: 50px;">)</div>
                                    </div>
                                    <div style="display: flex;">
                                        <div style="width: 70px">주 소</div>
                                        <div>대전광역시 유성구 문지로 272-37&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;http://www.stechinc.co.kr</div>
                                    </div>
                                    <div style="display: flex;">
                                        <div style="width: 70px">전 화</div>
                                        <div style="width: 130px;">(042)487-2421</div>
                                        <div style="width: 50px;">팩스</div>
                                        <div style="width: 130px;">(042)487-4421</div>
                                        <div style="width: 70px;">Email</div>
                                        <div style="width: 130px;">stechinc@stechinc.co.kr</div>
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                        <div class="report">
                            
                            <div class="content-header">
                                <div class="content-header-container">
                                    <div class="content-header-title" style="text-align: center;">
                                        <span style="font-size: 32px; font-weight: bold;">한국계측제어공업협동조합</span>
                                    </div>
                                </div>
                            </div>
                            <div class="content-body">
                                <div class="content-body-container">
                                    <div class="body-1">
                                        <table class="tb1">
                                            <colgroup>
                                                <col style="width: 45px;" />
                                                <col style="width: 65px;" /> 
                                                <col style="width: 30px;" />
                                                <col style="width: 75px;" />
                                                <col style="width: 30px;" />
                                                <col style="width: 75px;" />
                                                <col style="width: 110px;" />
                                            </colgroup>
                                            <tbody>
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
                                            </tbody>
                                        </table>
                                        <div>
                                            <div style="display: flex;">
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>문</span>
                                                    <span>서</span>
                                                    <span>번</span>
                                                    <span>호</span>
                                                </span>
                                                <span>&nbsp;: 계제 제&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;호</span>
                                            </div>
                                            <div style="height: 5px;"></div>
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
                                            <div style="display: flex;">    
                                                <span style="width: 70px; display: flex; justify-content: space-between;">
                                                    <span>제</span>
                                                    <span>목</span>
                                                </span>
                                                <span>&nbsp;: {{ vars.formData.project_management.project_name }} 관련 착수계 제출의 건 </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="body-2">
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
                                                <span>2. 귀&nbsp;</span>
                                                <span v-if="!vars.formState.readOnly">
                                                    <input type="text" v-model="vars.formData.attr03"> 
                                                    ({{ methods.contractData() }}) 우수조달공동상표 물품으로 계약 체곌한 "{{ vars.formData.project_management.project_name }}" 건과 관련하여 아래와 같이 납품완료계 및 관련 서류를 제출합니다.
                                                </span>
                                                <span v-else>
                                                    {{ vars.formData.attr03 }}&nbsp;
                                                    ({{ methods.contractData() }}) 우수조달공동상표 물품으로 계약 체결한 "{{ vars.formData.project_management.project_name }}" 건과 관련하여 아래와 같이 납품완료계 및 관련 서류를 제출합니다.
                                                </span>
                                            </div>
                                            <div style="width: 100%; padding: 10px; display: flex; flex-direction: column; gap: 8px;">
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">가.</div>
                                                    <div style="width: 90px;">계약 건명 :&nbsp;</div>
                                                    <div>{{ vars.formData.project_management.project_name }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">나.</div>
                                                    <div style="width: 90px;">계약 번호 :&nbsp;</div>
                                                    <div v-if="!vars.formState.readOnly"><input type="text" v-model="vars.formData.attr04"> (구매번호 : <input type="text" v-model="vars.formData.attr05">)</div>
                                                    <div v-else>{{ vars.formData.attr04 }} (구매번호 : {{ vars.formData.attr05 }})</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">다.</div>
                                                    <div style="width: 90px;">계약 금액 :&nbsp;</div>
                                                    <div>一金 {{ methods.companyAmountStr() }}정 (₩ {{ methods.companyAmount() }} VAT 포함)</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">라.</div>
                                                    <div style="width: 90px;">계약 일자 :&nbsp;</div>
                                                    <div>{{ methods.contractData() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">마.</div>
                                                    <div style="width: 90px;">착수 일자 :&nbsp;</div>
                                                    <div>{{ methods.commencementDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">바.</div>
                                                    <div style="width: 90px;">납품 일자 :&nbsp;</div>
                                                    <div>{{ methods.completionDate() }}</div>
                                                </div>
                                                <div style="width: 100%; display: flex;">
                                                    <div style="width: 30px;">사.</div>
                                                    <div style="width: 200px;">배정업체 세부사항&nbsp;</div>
                                                </div>
                                                <div style="width: 100%; display: flex; padding: 10px 30px;">
                                                    <table border="1">
                                                        <tbody>
                                                            <colgroup>
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                                <col style="width: 25%;" />
                                                            </colgroup>
                                                            <tr>
                                                                <td style="text-align: center;">업 체 명</td>
                                                                <td style="text-align: center;">에스텍아이앤씨(주)</td>
                                                                <td style="text-align: center;">대 표 자</td>
                                                                <td style="text-align: center;">박 길 현</td>
                                                            </tr>
                                                            <tr>
                                                                <td style="text-align: center;">주소</td>
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
                                                            <td rowspan="7" style="vertical-align: top;">첨부 </td>
                                                            <td>1.&nbsp;&nbsp;착수계 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>2.&nbsp;&nbsp;계약서 및 계약내역서 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>3.&nbsp;&nbsp;현장대리인계 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>4.&nbsp;&nbsp;배정업체 등록서류 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>5.&nbsp;&nbsp;시국세납입증명원 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>6.&nbsp;&nbsp;고용산재가입증명원 1부</td>
                                                        </tr>
                                                        <tr>
                                                            <td>7.&nbsp;&nbsp;예정공정표 1부 끝.</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="content-footer">
                                <div style="text-align: center;">
                                    <span style="font-weight: bold; font-size: 32px;">한국계측제어공업협동조합이사장</span>
                                </div>
                            </div>
                        </div>
                        <div class="report" style="font-size: 17px; font-weight: 500;">
                            
                            <div class="content-header" style="margin-top: 50px; margin-bottom: 50px;">
                                <div class="content-header-container">
                                    <div class="content-header-title" style="text-align: center;">
                                        <span style="font-size: 32px; font-weight: 400; border-bottom: 2px solid #000; padding-bottom: 5px; display: inline-block;">&nbsp;착&nbsp;&nbsp;&nbsp;&nbsp;수&nbsp;&nbsp;&nbsp;&nbsp;계&nbsp;</span>
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
                                            서울시 금천구 가산디지털2로 14, (대륭테크노타운12차 211호)
                                        </div>
                                        <div>
                                            한국계측제어공업협동조합
                                        </div>
                                        <div style="align-self: flex-end; display: flex; justify-content: space-between; width: 35%">
                                            <span style="">이</span>
                                            <span style="">시</span>    
                                            <span style="">장</span>
                                            <span style="">&nbsp;</span>
                                            <span style="">김</span>
                                            <span style="">영</span>
                                            <span style="">규</span>
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
import { reactive, onMounted, ref, watch, onUnmounted } from 'vue';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxTextBox from 'devextreme-vue/text-box';
import { projectRegistration, projectReport, projectConstruction } from '../../data-source/project';
import { alert } from 'devextreme/ui/dialog';
import { printReport } from '../../utils/print-report';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
export default {
    components: {
        DxTextBox,
        DxScrollView,
        DxPopup,
        DxToolbarItem,
        DxLoadPanel,
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
        vars.loading = ref(false);
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
                const DOCUMNET = [
                    '완료계 공문',
                    '계약서',
                    '계약내역서',
                    '현장대리인계',
                    '배정업체등록서류',
                    '시국세납입증명원',
                    '고용산재가입증명원',
                    '예정공정표',
                ]

                vars.loading.value = true;
                const { data : completionData} = await projectConstruction.load({ filter: [['fk_project_management_id', '=', props.fk_project_management_id]] });
                await printReport(DOCUMNET, completionData, document.querySelector('.measurement-construction-report'));
                vars.loading.value = false;
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