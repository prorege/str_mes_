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
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :visible="!props.mode"
            :options="{ 
                text: vars.dataSource.approvalStatus,
                icon: '', 
                onClick: methods.sendRequest 
            }"/>
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :visible="props.mode"
            :options="{ 
                text: '결재',
                icon: '', 
                onClick: methods.handleApproval,
                type: 'add',
            }"/>
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :visible="props.mode"
            :options="{ 
                text: '반려',
                icon: '', 
                onClick: methods.handleRejection,
                type: 'remove',
            }"/>
        <dx-toolbar-item 
            widget="dxButton" 
            toolbar="top" 
            location="after"
            :visible="!props.mode"
            :options="{ 
                text: '삭제',
                icon: '', 
                onClick: methods.handleDelete,
                type: 'remove',
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
                                    <td rowspan="3" style="writing-mode: vertical-rl; text-orientation: upright; letter-spacing: 0px;">결 재</td>
                                    <th style="width: 50px;" v-for="line in vars.dataSource.approvalLine" :key="line.id">{{ line.line_header }}</th>
                                </tr>
                                <tr style="height: 35px;">
                                    <td style="width: 50px;" v-for="line in vars.dataSource.approvalLine" :key="line.id">
                                        <div class="approval-sign-box">
                                        <img v-if="signImages[line.approval_employee?.id]?.hasImage" :src="signImages[line.approval_employee?.id]?.src" alt="" style="" class="approval-sign-image">
                                        <span>{{ line.approval_employee?.emp_name || '' }}</span>
                                        </div>
                                    </td>
                                </tr>
                                <tr style="height: 15px;">
                                    <td style="width: 50px;" v-for="line in vars.dataSource.approvalLine" :key="line.id">
                                        <div class="approval-sign-box">
                                            <span>{{ line.approval_date ? moment(line.approval_date).format('YYMMDD') : '' }}</span>
                                        </div>
                                    </td>
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
                                                    <span>{{ vars.formData.excution_plan_number }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>프로젝트번호</span>
                                                    <span>{{ vars.formData.project_management?.project_number }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>프로젝트명</span>
                                                    <span style="white-space: nowrap; overflow: hidden;">{{ vars.formData.project_management?.project_name }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-2">
                                                <div class="content-area-1-box-item">
                                                    <span>등록일자</span>
                                                    <span>{{ moment(vars.formData.excution_plan_date).format('YYYY.MM.DD') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>등록부서</span>
                                                    <span>{{ vars.formData.project_management?.excution_plan_department }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>등록담당자</span>
                                                    <span>{{ vars.formData.excution_plan_manager }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-3">
                                                <div class="content-area-1-box-item">
                                                    <span>결재상태</span>
                                                    <span>{{ vars.formData.approval_status }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>반려사유</span>
                                                    <span>{{ vars.formData.reject_reason }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-4">
                                                <div class="content-area-1-box-item">
                                                    <span>계약금액</span>
                                                    <span>{{ '₩' + numeral(vars.formData.contract_amount).format('0,0') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>예정금액</span>
                                                    <span>{{ '₩' + numeral(vars.formData.expect_amount).format('0,0') }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>실행금액</span>
                                                    <span>{{ '₩' + numeral(vars.formData.excution_amount).format('0,0') }}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="content-area-1-box item-5">
                                                <div class="content-area-1-box-item">
                                                    <span>계약대비예정률</span>
                                                    <span>{{ vars.formData.contract_to_expect_rate ? Number(vars.formData.contract_to_expect_rate).toFixed(1) + '%' : '' }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>예정대비실행률</span>
                                                    <span>{{ vars.formData.expect_to_excution_rate ? Number(vars.formData.expect_to_excution_rate).toFixed(1) + '%' : '' }}</span>
                                                </div>
                                                <div class="content-area-1-box-item">
                                                    <span>계약대비실행률</span>
                                                    <span>{{ vars.formData.contract_to_excution_rate ? Number(vars.formData.contract_to_excution_rate).toFixed(1) + '%' : '' }}</span>
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
                                                            <th style="text-align: right;">예정소요경비</th>
                                                            <th style="text-align: right;">소요경비</th>
                                                            <th style="text-align: center;">VAT</th>
                                                            <th style="text-align: right;">부가세</th>
                                                            <th style="text-align: left;">지출처</th>
                                                            <th style="text-align: center;">지출일자</th>
                                                            <th style="text-align: center;">등록자</th>
                                                            <th style="text-align: center;">등록일자</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr v-for="(item, itemIndex) in section.data" :key="`expense-${sectionIndex}-${itemIndex}`">
                                                            <td style="text-align: left;">{{ item.expense_description || '' }}</td>
                                                            <td style="text-align: right;">{{ item.expense_amount ? '₩' + numeral(item.expense_amount).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: right;">{{ item.excution_amount ? '₩' + numeral(item.excution_amount).format('0,0') : '₩ 0' }}</td>
                                                            <td style="text-align: center;">{{ item.vat_type || '' }}</td>
                                                            <td style="text-align: right;">{{ item.vat ? '₩' + numeral(item.vat).format('0,0') : '' }}</td>
                                                            <td style="text-align: left;">{{ item.expense_source || '' }}</td>
                                                            <td style="text-align: center;">{{ item.expense_date ? moment(item.expense_date).format('YYYY.MM.DD') : '' }}</td>
                                                            <td style="text-align: center;">{{ item.register || '' }}</td>
                                                            <td style="text-align: center;">{{ item.created ? moment(item.created).format('YYYY.MM.DD') : '' }}</td>
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
import { confirm, alert, custom } from 'devextreme/ui/dialog';
import numeral from 'numeral';
import moment from 'moment';
import { printReport } from '@/utils/print-report';
import { approval, approvalLine, getApproval, approvalLineResult } from '../../data-source/approval';
import { projectExcutionPlan, projectExcutionPlanItem, projectExcutionPlanSubcontract, projectExcutionPlanExpense } from '../../data-source/project';
import authService from '../../auth';
import { currentDateTime } from '@/utils/util';
import { notifyInfo, notifyError } from '../../utils/notify'

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
        excutionPlanId: {
            type: Number,
            default: null,
        },
        mode: {
            type: Boolean,
            default: false,
        },
        approvalData: {
            type: Object,
            default: null,
        }
    },
    emits: ['update:visible'],
    setup(props, { emit }) {
        const vars = {};
        vars.init = ref(false);
        vars.loading = ref(false);
    
        vars.dataSource = reactive({
            approvalLine: [],
            approvalStatus: "",
            approvalResult: null,
        });

        vars.formData = reactive({});
        vars.totalItms = reactive([]);
        const signImages = computed(() => {
        if (!vars.dataSource.approvalLine.length) return {};
        
        return vars.dataSource.approvalLine.reduce((acc, line, index) => {
            const key = line.approval_employee?.id;
            if (!key) return acc;

            if(line.closing_yn && line.approval_employee?.emp_sign_path){
                acc[key] = {
                    hasImage: true,
                    src: line.approval_employee?.emp_sign_path,
                };
            } else if (!line.closing_yn && line.approval_result == '반려'){
                acc[key] = {
                    hasImage: true,
                    src: '/api/mes/v1/file-manager/read/approval-attachment/반려.png/반려.png',
                };
            } else {
                acc[key] = {
                    hasImage: false,
                    src: '',
                };
            }

                return acc;
            }, {});
        });
        const methods = reactive({
            async initData() {
                await methods.resetData();
                if (props.excutionPlanId > 0) {

                    await methods.getApprovalStatus();
                    await methods.getApprovalLine();

                    let { data } = await projectExcutionPlan.byKey(props.excutionPlanId);
                    Object.assign(vars.formData, data);
                    let { data: planItems } = await projectExcutionPlanItem.load({ filter: [['fk_project_excution_plan_id', '=', props.excutionPlanId]] });
                    let { data: planSubcontracts } = await projectExcutionPlanSubcontract.load({ filter: [['fk_project_excution_plan_id', '=', props.excutionPlanId]] });
                    let { data: planExpenses } = await projectExcutionPlanExpense.load({ filter: [['fk_project_excution_plan_id', '=', props.excutionPlanId]] });


                    const planItemsSummary = planItems.length > 0 ? {
                        type: 'material_summary',
                        supply_price: '₩' + numeral(planItems.reduce((acc, item) => acc + item.supply_price, 0)).format('0,0'),
                        vat: '₩' + numeral(planItems.reduce((acc, item) => acc + item.vat, 0)).format('0,0'),
                        total_price: '₩' + numeral(planItems.reduce((acc, item) => acc + item.supply_price + item.vat, 0)).format('0,0'),
                        completion_price: '₩' + numeral(planItems.reduce((acc, item) => acc + item.purchase_supply_price, 0)).format('0,0'),
                    } : null;
                    const planSubcontractSummary = planSubcontracts.length > 0 ? {
                        type: 'subcontract_summary',
                        supply_price: '₩' + numeral(planSubcontracts.reduce((acc, item) => acc + item.expect_amount, 0)).format('0,0'),
                        vat: '₩' + numeral(planSubcontracts.reduce((acc, item) => acc + item.vat, 0)).format('0,0'),
                        total_price: '₩' + numeral(planSubcontracts.reduce((acc, item) => acc + item.expect_amount + item.vat, 0)).format('0,0'),
                        completion_price: '₩' + numeral(planSubcontracts.reduce((acc, item) => acc + item.purchase_unit_price, 0)).format('0,0'),
                    } : null;
                    const planExpenseSummary = planExpenses.length > 0 ? {
                        type: 'expense_summary',
                        supply_price: '₩' + numeral(planExpenses.reduce((acc, item) => acc + item.expense_amount, 0)).format('0,0'),
                        vat: '₩' + numeral(planExpenses.reduce((acc, item) => acc + item.vat, 0)).format('0,0'),
                        total_price: '₩' + numeral(planExpenses.reduce((acc, item) => acc + item.expense_amount + item.vat, 0)).format('0,0'),
                        completion_price: '₩' + numeral(planExpenses.reduce((acc, item) => acc + item.plan_amount, 0)).format('0,0'),
                    } : null;
                    if (planItems.length > 0) {
                        vars.totalItms.push( { type: 'material_title', title: '주요자재' })
                        vars.totalItms.push(
                            ...planItems.map(item => {
                                const clonedItem = JSON.parse(JSON.stringify(item));
                                clonedItem['type'] = 'material_data';
                                return clonedItem;
                            }) 
                        )
                        vars.totalItms.push(planItemsSummary);
                    }
                    if (planSubcontracts.length > 0) {
                        vars.totalItms.push( { type: 'subcontract_title', title: '외주공사' })
                        vars.totalItms.push(
                            ...planSubcontracts.map(item => {
                            const clonedItem = JSON.parse(JSON.stringify(item));
                            clonedItem['type'] = 'subcontract_data';
                            return clonedItem;
                            })
                        )
                        vars.totalItms.push(planSubcontractSummary);
                    }
                    if (planExpenses.length > 0) {
                        vars.totalItms.push( { type: 'expense_title', title: '경비' })
                        vars.totalItms.push(
                            ...planExpenses.map(item => {
                            const clonedItem = JSON.parse(JSON.stringify(item));
                            clonedItem['type'] = 'expense_data';
                            return clonedItem;
                            })
                        )
                        vars.totalItms.push(planExpenseSummary);
                    }
                    vars.init.value = true;
                }
                else {
                    vars.init.value = false;
                }

                if (props.approvalData) {
                    vars.dataSource.approvalResult = props.approvalData;
                }
            },
            async getApprovalStatus() {
                if (props.excutionPlanId > 0) {
                    getApproval([{ name: 'fk_excution_plan_id', op: 'eq', val: props.excutionPlanId || 0}, { name: 'fk_document_id', op: 'eq', val: 2}]).load().then((response) => {
                        console.log("response : ", response);
                        if(response.totalCount > 0){
                        vars.dataSource.approvalStatus = response.data[0]['approval_status'] || '상신요청';
                        } else {
                        vars.dataSource.approvalStatus = '상신요청';
                        }
                    }).catch((error) => {
                        vars.dataSource.approvalStatus = '오류';
                    })
                }
            },
            async getApprovalLine() {
                try {
                    const { data : approvalData } = await approval.load({
                        filter: [
                            ['fk_excution_plan_id', '=', props.excutionPlanId],
                            ['fk_document_id', '=', 2]
                        ]
                    })
                    if (approvalData.length > 0) {
                        vars.dataSource.approvalLine = approvalData[0].approval_line_result;
                    } else {
                        const { data : approvalLineData } = await approvalLine.load({
                            filter: [
                                ['fk_request_emp_id', '=', authService.user?.emp_id || 0],
                                'and',
                                ['fk_document_id', '=', 2]
                            ],
                            sort: [
                                {
                                    selector: 'line_order',
                                    desc: false
                                }
                            ]
                        });
                        if (approvalLineData.length > 0) {
                            vars.dataSource.approvalLine = approvalLineData;
                        }
                        else {
                            vars.dataSource.approvalLine = [];
                        }
                    }
                }
                catch (error) { 
                    console.error('getApprovalLine error:', error);
                }
            },
            async resetData() {
                vars.totalItms.length = 0;
                Object.keys(vars.formData).forEach(key => delete vars.formData[key]);
            },
            async printReport() {
                vars.loading.value = true;
                await printReport('', [], document.querySelector('.excution-report'));
                vars.loading.value = false;
            },
            async sendRequest() {
                if (vars.dataSource.approvalStatus != '상신요청') {
                    alert('상신요청이 완료되었습니다.', '상신요청 완료');
                    return;
                }
                if (!vars.formData.id) {
                    alert('등록된 데이터가 없습니다. 먼저 데이터를 등록해주세요.', '데이터 미등록');
                    return;
                }

                if (vars.dataSource.approvalLine.length == 0) {
                    alert('결재선이 존재하지 않습니다. 결재선을 지정해주세요.', '결재선 지정');
                    return;
                }
              
                const result = await confirm('상신하시겠습니까?', '상신');
                if (!result) return;
                
                vars.loading.value = true;

                try {
                    const approvalFormData = {
                        document_name : '사업실행계획보고서',
                        fk_excution_plan_id: props.excutionPlanId,
                        fk_company_id: authService.getCompanyId(),
                        fk_document_id: 2,
                        approval_date: currentDateTime(),
                        approval_status: '상신완료',
                        approval_document: {id: 2},
                        fk_request_emp_id: authService.user?.emp_id,
                    }
                    const { data : approvalData } = await approval.insert(approvalFormData);
                    if (approvalData.id) {  
                        let count = 0;
                        for (const line of vars.dataSource.approvalLine) {

                            const arFormData = {
                                line_header: line.line_header,
                                approval_result: '대기중',
                                fk_approval_id: approvalData.id,
                                fk_approval_line_id: line.id,
                                fk_approval_emp_id: line.fk_approval_emp_id,
                                fk_request_emp_id: line.fk_request_emp_id,
                            }
                            if (count == 0) {
                                arFormData.active_yn = true;
                            }
                            count++;
                            const { data : approvalLineResultData } = await approvalLineResult.insert(arFormData);
                        }
                        vars.dataSource.approvalStatus = '상신완료';
                        notifyInfo('상신 요청이 완료 됐습니다.');
                    }
                    else {
                        notifyError('상신 요청 중 오류가 발생했습니다.');
                    }
                }
                catch (error) {
                    console.error('sendRequest error:', error);
                    notifyError('상신 요청 중 오류가 발생했습니다.');
                }
                finally{
                    vars.loading.value = false;
                }
            },
            async handleApproval(data){
               
                const resultData = vars.dataSource.approvalResult;
                if(resultData.approval_result == '결재완료'){
                    alert('이미 결재가 완료 됐습니다.', '결재');
                    return;
                }
                let isSelect = await confirm('결재 하시겠습니까?', '결재');
                if (!isSelect) {
                    return;
                }
                try {
                    await approvalLineResult.update(resultData.id, {'approval_result': '결재완료', 'approval_reason': '', 'closing_yn': true, 'approval_date': moment().format('YYYY-MM-DD HH:mm:ss')})
                    await approval.update(resultData.fk_approval_id, {'approval_reason': ''});
                    vars.dataSource.approvalResult.approval_result = '결재완료';
                    await methods.getApprovalLine();
                    notifyInfo('결재처리가 완료되었습니다');
                }catch (ex) {
                    console.error(ex);
                }
            },
            async handleRejection(data){
                const resultData = vars.dataSource.approvalResult;
                const { data : _approval } = await approval.byKey(resultData.fk_approval_id);
                const _approvalLineResult = _approval.approval_line_result;
        
                const currentIndex = _approvalLineResult.findIndex(item => item.id == resultData.id);
                const nextItem = _approvalLineResult[currentIndex + 1] || null;

                if (nextItem && (nextItem.approval_result == '결재완료' || nextItem.approval_result == '반려')) {
                    alert('이미 상위 결재자가 결재 또는 반려를 완료했습니다.', '반려');
                    return;
                }

                if(resultData.approval_result == '반려'){
                    alert('이미 반려가 완료 됐습니다.', '반려');
                    return;
                }
                let isSelect = await confirm('반려 하시겠습니까?', '반려');
                if (!isSelect) {
                    return;
                }
                custom({
                    title: '반려사유',
                    messageHtml: `
                        <div>
                            <label for="rejectionReason">반려 사유:</label>
                            <input type="text" id="rejectionReason" placeholder="반려 사유를 입력하세요" 
                                    style="width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;" maxlength="300" />
                        </div>
                    `,
                    buttons: [
                        { text: '확인', onClick: () => {
                        const rejectionReason = document.getElementById('rejectionReason').value;
                        return rejectionReason;
                        } },
                        { text: '취소', onClick: () => {
                        return null;
                        } }
                    ],
                }).show().then(async (result) => {
                if (result !==  null) {
                    const params = {
                        'approval_result': '반려',
                        'approval_reason': result,
                        'closing_yn': false,
                        'active_yn': 1,
                        'approval_date': moment().format('YYYY-MM-DD HH:mm:ss')
                    }
                    await approvalLineResult.update(resultData.id, params)
                    if (nextItem) {
                        await approvalLineResult.update(nextItem.id, {'active_yn': 0});
                    }
                    await approval.update(resultData.fk_approval_id, {'approval_reason': result})
                    vars.dataSource.approvalResult.approval_result = '반려';
                    await methods.getApprovalLine();
                    notifyInfo('반려처리가 완료되었습니다');
                }else{
                    notifyInfo('반려처리가 취소되었습니다');
                }
                });
            },
            async handleDelete() {
                if (vars.dataSource.approvalStatus == '상신요청') {
                    alert("결재가 존재하지않습니다.", "삭제");
                    return;
                }
                const result = await confirm('삭제하시겠습니까?', '삭제');
                if (!result) return;
                try {
                    approval.load({ filter: [['fk_excution_plan_id', '=', props.excutionPlanId], ['fk_document_id', '=', 2]] }).then(async (response) => {
                        if (response.totalCount > 0) {
                            const _find = response.data[0].approval_line_result.find(item => item.approval_result !== "대기중");
                            if (_find) {
                                alert("결재가 진행되었습니다. 삭제가 불가능합니다.", "삭제");
                                return;
                            }
                            for (const item of response.data[0]['approval_line_result']) {
                                await approvalLineResult.remove(item.id);
                            }
                            await approval.remove(response.data[0].id);
                            notifyInfo('삭제 완료되었습니다.');
                            emit('update:visible', false);
                        }
                    });
                }
                catch (error) {
                    console.error('handleDelete error:', error);
                    notifyError('삭제 중 오류가 발생했습니다.');
                }
       
            }
        });
    
        const sections = computed(() => {
            if (!vars.totalItms) return [];
            
            const result = [];
            let currentSection = null;
            
            for (const item of vars.totalItms) {
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
            sections,
            signImages,
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
            width: 100%;
            display: flex;
            justify-content: right;
            
            .approval-line-table {
                width: auto; // 콘텐츠에 맞게 자동 조정
                border-collapse: collapse;
                border: 1px solid #000;
                .approval-sign-box {
                    position: relative;
                    .approval-sign-image {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        width: 35px;
                        height: 35px;
                        opacity: 0.7;   
                    }
                }
            }
            
            tr th, td {
                border-right: 1px solid #000;
                border-bottom: 1px solid #000;
                text-align: center;
                font-size: 10px;
            }
            .approval-line-table tr th:last-child,
            .approval-line-table tr td:last-child {
                border-right: none;
            }
            .approval-line-table tr:last-child th,
            .approval-line-table tr:last-child td {
                border-bottom: none;
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
            width: 100%;
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
                    border: 1pt solid #cfcfcf;
                    tr {
                        th, td {
                            box-sizing: border-box;
                            border-right: 1pt solid #cfcfcf !important;
                            border-bottom: 1pt solid #cfcfcf !important;
                            padding: 2px;
                            white-space: nowrap;
                        }
                        th {
                            background-color: #f0f0f0;
                        }
                    }
                    tr th:last-child,
                    tr td:last-child {
                        border-right: none !important;
                    }
                    tr:last-child th,
                    tr:last-child td {
                        border-bottom: none !important;
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