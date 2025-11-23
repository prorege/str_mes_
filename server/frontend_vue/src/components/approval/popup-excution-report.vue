<template>
    <dx-popup
        :visible="props.visible"
        content-template="popup-content"
        title="사업실행보고서"
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
        <template #popup-content>
            <dx-scroll-view width="100%" height="100%">
                <dx-load-panel :visible="vars.loading.value" :show-pane="true" />
                <div v-if="vars.init" class="excution-report">
                    <div class="report">
                        <div class="content-header">
                            <div class="content-header-title">
                                <span>사업실행보고서</span>
                            </div>
                        </div>
                        <div class="content-header-approval-line">
                            <table class="approval-line-table">
                                <tr>
                                    <td rowspan="2" style="writing-mode: vertical-rl; text-orientation: upright; letter-spacing: 0px;">결 재</td>
                                    <!-- <th v-for="line in vars.dataSource.approvalLine" :key="line.id">{{ line.line_header }}</th> -->
                                    <td>기 안</td>
                                    <td>팀 장</td>
                                    <td>실 장</td>
                                    <td>대표이사</td>
                                </tr>
                                <tr style="height: 35px;">
                                    <!-- <td v-for="line in vars.dataSource.approvalLine" :key="line.id">
                                        <div class="approval-sign-box">
                                        <img v-if="signImages[line.approval_employee?.id]?.hasImage" :src="signImages[line.approval_employee?.id]?.src" alt="" style="" class="approval-sign-image">
                                        <span>{{ line.approval_employee?.emp_name || '' }}</span>
                                        </div>
                                    </td> -->
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                </tr>
                                <tr style="height: 20px;">
                                    <!-- <td v-for="line in vars.dataSource.approvalLine" :key="line.id">
                                    <div class="approval-sign-box">
                                        <span>{{ line.approval_date ? moment(line.approval_date).format('YYMMDD') : '' }}</ span>
                                    </div>
                                    </td> -->
                                    <td>날짜</td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                </tr>
                            </table>
                        </div>
                        <div class="content-body">
                            <div class="content-area-1">
                                <table>
                                    <colgroup>
                                        <col style="width: 30%;" />
                                        <col style="width: 20%;" />
                                        <col style="width: 16%;" />
                                        <col style="width: 18%;" />
                                        <col style="width: 16%;" />
                                    </colgroup>
                                    <tr>
                                        <td>
                                            <div class="content-area-1-box item-1">
                                                <div class="content-area-1-box-item">
                                                    <span>실행계획번호</span>
                                                    <span>{{ props.data.formData.excution_plan_number }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>프로젝트번호</span>
                                                    <span>{{ props.data.formData.project_management.project_number }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>프로젝트명</span>
                                                    <span style="white-space: nowrap; overflow: hidden;">{{ props.data.formData.project_management.project_name }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-2">
                                                <div class="content-area-1-box-item">
                                                    <span>등록일자</span>
                                                    <span>{{ moment(props.data.formData.excution_plan_date).format('YYYY.MM.DD') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>등록부서</span>
                                                    <span>{{ props.data.formData.project_management.excution_plan_department }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>등록담당자</span>
                                                    <span>{{ props.data.formData.excution_plan_manager }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-3">
                                                <div class="content-area-1-box-item">
                                                    <span>결재상태</span>
                                                    <span>{{ props.data.formData.approval_status }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>반려사유</span>
                                                    <span>{{ props.data.formData.reject_reason }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-4">
                                                <div class="content-area-1-box-item">
                                                    <span>계약금액</span>
                                                    <span>{{ '₩' + numeral(props.data.formData.contract_amount).format('0,0') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>예정금액</span>
                                                    <span>{{ '₩' + numeral(props.data.formData.expect_amount).format('0,0') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>실행금액</span>
                                                    <span>{{ '₩' + numeral(props.data.formData.excution_amount).format('0,0') }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-5">
                                                <div class="content-area-1-box-item">
                                                    <span>계약대비예정률</span>
                                                    <span>{{ props.data.formData.contract_to_expect_rate ? Number(props.data.formData.contract_to_expect_rate).toFixed(1) + '%' : '' }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>예정대비실행률</span>
                                                    <span>{{ props.data.formData.expect_to_excution_rate ? Number(props.data.formData.expect_to_excution_rate).toFixed(1) + '%' : '' }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>계약대비실행률</span>
                                                    <span>{{ props.data.formData.contract_to_excution_rate ? Number(props.data.formData.contract_to_excution_rate).toFixed(1) + '%' : '' }}</span>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <div style="margin-top: 10px; margin-bottom: 10px;">
                                <div style="text-align: center; background-color: #f0f0f0; height: 40px; line-height: 40px;">원 가 내 역</div>
                            </div>
                            <div class="content-area-2">
                                <table>
                                    <tbody v-for="(section, sectionIndex) in sections" :key="sectionIndex">
                                        <!-- 제목 -->
                                        <tr>
                                            <td style="font-weight: bold; font-size: 12px;">{{ section.title }}</td>
                                        </tr>
                                        <!-- 데이터 테이블 -->
                                        <tr>
                                            <td>
                                                <!-- 주요자재 테이블 -->
                                                <table v-if="section.type === 'material'" class="tb2">
                                                    <thead>
                                                        <tr>
                                                            <th width="55px" style="text-align: left;">품목코드</th>
                                                            <th width="120px" style="text-align: left;">제품명</th>
                                                            <th style="text-align: left;">규격</th>
                                                            <th width="90px" style="text-align: left;">구매처</th>
                                                            <th width="40px" style="text-align: center;">발주수량</th>
                                                            <th width="55px" style="text-align: right;">예정단가</th>
                                                            <th width="55px" style="text-align: right;">발주단가</th>
                                                            <th width="55px" style="text-align: right;">예정금액</th>
                                                            <th width="55px" style="text-align: right;">발주금액</th>
                                                            <th width="45px" style="text-align: right;">부가세</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(item, itemIndex) in section.data" :key="`material-${sectionIndex}-${itemIndex}`">
                                                            <td style="text-align: left;">{{ item.item_code || '' }}</td>
                                                            <td style="text-align: left;">{{ item.item.item_name || '' }}</td>
                                                            <td style="text-align: left;">{{ item.item.item_standard || '' }}</td>
                                                            <td style="text-align: left;">{{ item.main_supplier || '' }}</td>
                                                            <td style="text-align: center;">{{ item.excution_plan_quantity ? numeral(item.excution_plan_quantity).format('0,0') : '0' }}</td>
                                                            <td style="text-align: right;">{{ item.unit_price ? '₩' + numeral(item.unit_price).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.purchase_unit_price ? '₩' + numeral(item.purchase_unit_price).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.supply_price ? '₩' + numeral(item.supply_price).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.purchase_supply_price ? '₩' + numeral(item.purchase_supply_price).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.vat ? '₩' + numeral(item.vat).format('0,0') : '₩ 0' }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <!-- 외주공사 테이블 -->
                                                <table v-else-if="section.type === 'subcontract'" class="tb2">
                                                    <thead>
                                                        <tr>
                                                            <th style="text-align: left;">공사명</th>
                                                            <th style="text-align: left;">공사업체</th>
                                                            <th style="text-align: right;">예정가격</th>
                                                            <th style="text-align: right;">발주단가</th>
                                                            <th style="text-align: center;">VAT</th>
                                                            <th style="text-align: right;">부가세</th>
                                                            <th style="text-align: center;">견적서</th>
                                                            <th style="text-align: center;">등록자</th>
                                                            <th style="text-align: center;">등록일자</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(item, itemIndex) in section.data" :key="`subcontract-${sectionIndex}-${itemIndex}`">
                                                            <td style="text-align: left;">{{ item.subcontract_name || '' }}</td>
                                                            <td style="text-align: left;">{{ item.subcontract_company || '' }}</td>
                                                            <td style="text-align: right;">{{ item.expect_amount ? '₩' + numeral(item.expect_amount).format('0,0') : '' }}</td>
                                                            <td style="text-align: right;">{{ item.purchase_unit_price ? '₩' + numeral(item.purchase_unit_price).format('0,0') : '' }}</td>
                                                            <td style="text-align: center;">{{ item.vat_type || '' }}</td>
                                                            <td style="text-align: right;">{{ item.vat ? '₩' + numeral(item.vat).format('0,0') : '' }}</td>
                                                            <td style="text-align: center;">{{ item.estimate_document || '' }}</td>
                                                            <td style="text-align: center;">{{ item.register || '' }}</td>
                                                            <td style="text-align: center;">{{ item.created ? moment(item.created).format('YYYY.MM.DD') : '' }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <!-- 경비 테이블 -->
                                                <table v-else-if="section.type === 'expense'" class="tb2">
                                                    <thead>
                                                        <tr>
                                                            <th style="text-align: left;">경비내역</th>
                                                            <th style="text-align: left;">예정소요경비</th>
                                                            <th style="text-align: right;">소요경비</th>
                                                            <th style="text-align: right;">VAT</th>
                                                            <th style="text-align: right;">부가세</th>
                                                            <th style="text-align: right;">지출처</th>
                                                            <th style="text-align: right;">지출일자</th>
                                                            <th style="text-align: right;">등록자</th>
                                                            <th style="text-align: right;">등록일자</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(item, itemIndex) in section.data" :key="`expense-${sectionIndex}-${itemIndex}`">
                                                            <td style="text-align: left;">{{ item.expense_description || '' }}</td>
                                                            <td style="text-align: left;">{{ item.expense_amount ? '₩' + numeral(item.expense_amount).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.excution_amount ? '₩' + numeral(item.excution_amount).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.vat_type || '' }}</td>
                                                            <td style="text-align: right;">{{ item.vat ? '₩' + numeral(item.vat).format('0,0') : '' }}</td>
                                                            <td style="text-align: right;">{{ item.expense_source || '' }}</td>
                                                            <td style="text-align: right;">{{ item.expense_date ? moment(item.expense_date).format('YYYY.MM.DD') : '' }}</td>
                                                            <td style="text-align: right;">{{ item.register || '' }}</td>
                                                            <td style="text-align: right;">{{ item.created ? moment(item.created).format('YYYY.MM.DD') : '' }}</td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <!-- 합계 테이블 -->
                                        <tr v-if="section.summary">
                                            <td>
                                                <table style="width: 60%;">
                                                    <tr>
                                                        <th>예정 공급가</th>
                                                        <td>{{ section.summary.supply_price || '' }}</td>
                                                        <th>예정 부가세</th>
                                                        <td>{{ section.summary.vat || '' }}</td>
                                                        <th>예정 합계금액</th>
                                                        <td>{{ section.summary.total_price || '' }}</td>
                                                        <th>실행금액</th>
                                                        <td>{{ section.summary.completion_price || '' }}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div>

                    </div>
                </div>
            </dx-scroll-view>
        </template>
    </dx-popup> 
</template>
<script>
import { reactive, onMounted, ref, watch, onUnmounted, computed } from 'vue';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import numeral from 'numeral';
import moment from 'moment';
import { printReport } from '@/utils/print-report';

export default {
    components: {
        DxPopup,
        DxToolbarItem,
        DxLoadPanel,
        DxScrollView,
    },
    props: {
        visible: {
            type: Boolean,
            default: false,
        },
        data: {
            type: Object,
            default: null,
        },
    },
    emits: ['update:visible'],
    setup(props, { emit }) {
        const vars = {};
        vars.init = ref(false);
        vars.loading = ref(false);
    
        const methods = reactive({
            async initData() {
                
                vars.init.value = true;

            },
            async printReport() {
                vars.loading.value = true;
                await printReport('', [], document.querySelector('.excution-report'));
                vars.loading.value = false;
            },
        });
    
        const sections = computed(() => {
            if (!props.data?.totalItms) return [];
            
            const result = [];
            let currentSection = null;
            
            for (const item of props.data.totalItms) {
                if (item.type.endsWith('_title')) {
                    if (currentSection) {
                        result.push(currentSection);
                    }
                    currentSection = {
                        title: item.title,
                        type: item.type.replace('_title', ''),
                        data: [],
                        summary: null
                    };
                } else if (item.type.endsWith('_data')) {
                    if (currentSection) {
                        currentSection.data.push(item);
                    }
                } else if (item.type.endsWith('_summary')) {
                    if (currentSection) {
                        currentSection.summary = item;
                        result.push(currentSection);
                        currentSection = null;
                    }
                }
            }
            
            if (currentSection) {
                result.push(currentSection);
            }
            
            return result;
        });
        
        watch(
            () => props.visible,
            () => {
                if (props.visible) {
                    methods.initData();
                } else {
                    vars.init.value = false;
                }
            }, { immediate: true }
        );
        return {
            vars,
            methods,
            props,
            emit,
            numeral,
            moment,
            sections
        };
    },
};
</script>

<style lang="scss">
.excution-report {
    .report {
        font-family: '맑은 고딕', 'Malgun Gothic', sans-serif; 
        -webkit-print-color-adjust: exact; 
        width: 210mm; 
        height: 297mm; 
        box-sizing: border-box; 
        padding: 8px;
        font-size: 15px;
        border: 1px dotted #9c9c9c;
        table {width: 100%; border-collapse: collapse; table-layout: fixed;}
        .content-header {
            margin-top: 20px;
            margin-bottom: 10px;
            display: flex;
            width: 100%;
            justify-content: center;
            
    
            .content-header-title {
                font-size: 30px;
                font-weight: 400;
                text-align: center;
            }

        }
        .content-header-approval-line {
            width: 98%;
            display: flex;
            justify-content: right;
            
            .approval-line-table {
                width: auto; // 콘텐츠에 맞게 자동 조정
            }
            
            tr th, td {
                border : 1px solid #000;
                text-align: center;
                font-size: 10px;
            }
            
            tr:first-child {
                td[rowspan="2"] {
                    width: 25px !important;
                    min-width: 25px;
                    max-width: 25px;
                    text-align: center; 
                    vertical-align: middle;
                }
                
                td:not([rowspan]) {
                    width: 50px !important;
                    min-width: 50px;
                    max-width: 50px;
                }
            }
        }
        .content-body {
            margin-top: 20px;
            width: 98%;
            .content-area-1 {
                width: 100%;
                background-color: #F7F7F7;
                border-radius: 5px;
                padding: 5px;
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 10px;
                    
                    tr {
                        height: auto; 
                        td {
                            height: 100%;
                            vertical-align: top; 
                            padding: 5px;
                        }
                    }
                }
                .content-area-1-box {
                    min-height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start; 
                    align-items: flex-start;
                    gap: 5px;
                    .content-area-1-box-item {
                        width: 100%;
                        display: flex;
                        flex-direction: row;
                        gap: 10px;
                        span:first-child {
                            padding: 3px 0px 3px 0px;
                        }
                        span:last-child {
                            background-color: #FFFFFF;
                            border-radius: 3px;
                            padding: 3px;
                        }
                    }
                    
                    &.item-1 {
                        .content-area-1-box-item {
                            span:first-child {
                                width: 28%;
                                flex-shrink: 0;
                            }
                            span:last-child {
                                width: 72%;
                            }
                        }
                    }
                    &.item-2 {
                        .content-area-1-box-item {
                            span:first-child {
                                width: 36%;
                                flex-shrink: 0;
                            }
                            span:last-child {
                                width: 64%;
                            }
                        }
                    }
                    &.item-3 {
                        .content-area-1-box-item {
                            span:first-child {
                                width: 45%;
                                flex-shrink: 0;
                            }
                            span:last-child {
                                width: 55%;
                            }
                        }
                    }
                    &.item-4 {
                        .content-area-1-box-item {
                            span:first-child {
                                width: 35%;
                                flex-shrink: 0;
                            }
                            span:last-child {
                                width: 65%;
                            }
                        }
                    }
                    &.item-5 {
                        .content-area-1-box-item {
                            span:first-child {
                                width: 64%; 
                                flex-shrink: 0;
                            }
                            span:last-child {
                                width: 36%;
                            }
                        }
                    }
                    
                }
            }
            .content-area-2 {
                box-sizing: border-box;
                table {
                    font-size: 8px;
                }
                .tb2 {
                    tr {
                        th, td {
                            box-sizing: border-box;
                            border: 1pt solid #f0f0f0e1 !important;
                            padding: 2px;
                            white-space: nowrap;
                        }
                        th {
                            background-color: #f0f0f0;
                        }
                    }
                }
            }
        }
    }
    
    /* 인쇄용 스타일 */
    @media print {
        .report {
            page-break-inside: avoid;
        }
        .tb2 {
            page-break-inside: auto;
        }
        .tb2 thead {
            display: table-header-group;
        }
        .tb2 tbody tr {
            page-break-inside: avoid;
        }
        .tb2 td, .tb2 th {
            page-break-inside: avoid;
        }
    }
}
</style>