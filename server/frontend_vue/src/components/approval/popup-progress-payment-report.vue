<template>
    <dx-popup
        :visible="props.visible"
        content-template="popup-content"
        title="사업실행보고서"
        :resize-enabled="true"
        :close-on-outside-click="true"
        @update:visible="(value) => emit('update:visible', value)"
        width="310mm"
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
                <div v-if="vars.init" class="progress-payment-report">
                    <div class="report">
                        <div class="content-header">
                            <div class="content-header-title">
                                <span style="border-bottom: 2px solid #000; letter-spacing: 5px;">&nbsp;{{ currentMonth }}月기성고검토보고서&nbsp;</span>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; width: 100%;">
                            <div class="content-header-approval-line">
                                <table class="approval-line-table" v-if="vars.dataSource.approvalLine.length > 0">
                                    <tr>
                                        <th class="bg-gray" :colspan="vars.dataSource.approvalLine.length + 1">경영지원팀</th>
                                    </tr>
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
                            <div class="content-header-approval-line">
                                <table class="approval-line-table" v-if="vars.dataSource.approvalLine2.length > 0">
                                    <tr>
                                        <th class="bg-gray" :colspan="vars.dataSource.approvalLine2.length + 1">담당 부서</th>
                                    </tr>
                                    <tr>
                                        <td rowspan="3" style="writing-mode: vertical-rl; text-orientation: upright; letter-spacing: 0px;">결 재</td>
                                        <th style="width: 50px;" v-for="line in vars.dataSource.approvalLine2" :key="line.id">{{ line.line_header }}</th>
                                    </tr>
                                    <tr style="height: 35px;">
                                        <td style="width: 50px;" v-for="line in vars.dataSource.approvalLine2" :key="line.id">
                                            <div class="approval-sign-box">
                                            <img v-if="signImages[line.approval_employee?.id]?.hasImage" :src="signImages[line.approval_employee?.id]?.src" alt="" style="" class="approval-sign-image">
                                            <span>{{ line.approval_employee?.emp_name || '' }}</span>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr style="height: 15px;">
                                        <td style="width: 50px;" v-for="line in vars.dataSource.approvalLine2" :key="line.id">
                                            <div class="approval-sign-box">
                                                <span>{{ line.approval_date ? moment(line.approval_date).format('YYMMDD') : '' }}</span>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                        
                        <div class="content-body">
                            <div class="content-area-1">
                                <table>
                                    <colgroup>
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                        <col style="width: 12.5%;" />
                                    </colgroup>
                                    <tbody>
                                        <tr>
                                            <th class="bg-gray" colspan="1">사업번호</th>
                                            <td colspan="3">{{ vars.formData.project_number || '' }}</td>
                                            <th class="bg-gray" colspan="1">준공일(예정일)</th>
                                            <td colspan="3">{{ vars.formData.completion_date ? moment(vars.formData.completion_date).format('YYYY-MM-DD') : '' }}</td>
                                        </tr>
                                        <tr>
                                            <th class="bg-gray" colspan="1">사업명</th>
                                            <td colspan="3">{{ vars.formData.project_name || '' }}</td>
                                            <th class="bg-gray" colspan="1">담당PM</th>
                                            <td colspan="1">{{ vars.formData.project_manager || '' }}</td>
                                            <th class="bg-gray" colspan="1">작성일</th>
                                            <td colspan="1">{{ vars.formData.project_date ? moment(vars.formData.project_date).format('YYYY-MM-DD') : '' }}</td>
                                        </tr>
                                        <tr>
                                            <th class="bg-gray" colspan="1">고객사</th>
                                            <td colspan="3">{{ vars.formData.contract_company || '' }}</td>
                                            <th class="bg-gray" colspan="1">협력사(발주)</th>
                                            <td colspan="3">{{ vars.dataSource.projectExcutionPlanSubcontract?.subcontract_company || '' }}</td>
                                        </tr>
                                        <tr>
                                            <th class="bg-gray" colspan="1">계약금액</th>
                                            <td colspan="2" style="border-right: none !important; text-align:center;">{{ vars.formData.company_amount ? '₩ ' + numeral(vars.formData.company_amount).format('0,0') : '₩ 0' }}</td>
                                            <td colspan="1" style="text-align: right; border-left: none !important;">(VAT 별도)</td>
                                            <th class="bg-gray" colspan="1">계약금액</th>
                                            <td colspan="2" style="border-right: none !important; text-align:center;">{{ vars.dataSource.projectExcutionPlanSubcontract?.expect_amount ? '₩ ' + numeral(vars.dataSource.projectExcutionPlanSubcontract?.expect_amount).format('0,0') : '₩ 0' }}</td>
                                            <td colspan="1" style="text-align: right; border-left: none !important;">(VAT 별도)</td>
                                        </tr> 
                                    </tbody>
                                </table>
                            </div>
                            <div class="content-area-2" style="">
                                <table style="width: 50%; margin-right: 3px;">
                                    <colgroup>
                                        <col style="width: 5%;" />
                                        <col style="width: 20%;" />
                                        <col style="width: 25%;" />
                                        <col style="width: 25%;" />
                                        <col style="width: 25%;" />
                                    </colgroup>
                                    <tbody>
                                        <tr>
                                            <th colspan="5">에스텍아이앤씨</th>
                                        </tr>
                                        <tr>
                                            <th class="bg-gray" colspan="1">NO</th>
                                            <th class="bg-gray" colspan="1">계산서발행일</th>
                                            <th class="bg-gray" colspan="2">청구금액</th>
                                            <th class="bg-gray" colspan="1">누계요율</th>
                                        </tr>
                                        <tr v-for="(item, index) in vars.dataSource.projectCostLog" :key="item?.id || `empty-${index}`">
                                            <td colspan="1" style="text-align: center;">{{ index + 1 }}</td>
                                            <td colspan="1" style="text-align: center;">{{ item?.cost_date ? moment(item.cost_date).format('YYYY-MM-DD') : '' }}</td>
                                            <td colspan="2" style="text-align: right;">
                                                {{ item?.curr_cost ? '₩ ' + numeral(item.curr_cost).format('0,0') : '' }}
                                            </td>
                                            <td colspan="1" style="text-align: center;">{{ item?.total_cost_rate ? numeral(item.total_cost_rate).format('0.0%') : '' }}</td>
                                        </tr>
                                        <tr style="border: 2px solid #000000;">
                                            <th colspan="2" style="text-align: center;">누계</th>
                                            <th colspan="2" style="text-align: right;">
                                                {{ vars.dataSource.projectCostLog && vars.dataSource.projectCostLog.length > 0 ? '₩ ' + numeral(vars.dataSource.projectCostLog.filter(item => item && item.curr_cost).reduce((acc, item) => acc + (item.curr_cost || 0), 0)).format('0,0') : '₩ 0' }}
                                            </th>
                                            <th colspan="1" style="text-align: center;">
                                                {{ vars.dataSource.projectCostLog && vars.dataSource.projectCostLog.length > 0 ? numeral(vars.dataSource.projectCostLog[vars.dataSource.projectCostLog.length - 1].total_cost_rate).format('0.0%') : '0%' }}
                                            </th>
                                        </tr>
                                        <tr class="no-border-row">
                                            <td colspan="5" style="padding-top: 20px; padding-bottom: 20px; padding-left: 10px;">※ 특기사항 : 자재발주 관련하여 긴급자금 지급 요청으로 즉시 지급이 필요함.</td>
                                        </tr>
                                        <tr style="border-top: 2pt solid #000000;">
                                            <th colspan="3">에스텍아이앤씨 잔여기성</th>
                                            <th style="text-align: right;">{{ vars.dataSource.projectCostLog && vars.dataSource.projectCostLog.length > 0 ? '₩ ' + numeral(vars.dataSource.projectCostLog[vars.dataSource.projectCostLog.length - 1].remaining_cost).format('0,0') : '₩ 0' }}</th>
                                            <th style="text-align: center;">{{ vars.dataSource.projectCostLog && vars.dataSource.projectCostLog.length > 0 ? numeral((1 - vars.dataSource.projectCostLog[vars.dataSource.projectCostLog.length - 1].total_cost_rate) * 100).format('0.0') + '%' : '100%' }}</th>
                                        </tr>
                                    </tbody>
                                </table>
                                <table style="width: 50%;">
                                    <colgroup>
                                        <col style="width: 5%;" />
                                        <col style="width: 20%;" />
                                        <col style="width: 25%;" />
                                        <col style="width: 25%;" />
                                        <col style="width: 25%;" />
                                    </colgroup>
                                    <tbody>
                                        <tr>
                                            <th colspan="5">{{ vars.dataSource.projectExcutionPlanSubcontract?.subcontract_company || '' }}</th>
                                        </tr>
                                        <tr>
                                            <th class="bg-gray" colspan="1">NO</th>
                                            <th class="bg-gray" colspan="1">기성청구일</th>
                                            <th class="bg-gray" colspan="2">금회 청구금액</th>
                                            <th class="bg-gray" colspan="1">요율</th>
                                        </tr>
                                        <tr v-for="(item, index) in vars.dataSource.projectOutCostLog" :key="item?.id || `empty-${index}`">
                                            <td colspan="1" style="text-align: center;">{{ index + 1 }}</td>
                                            <td colspan="1" style="text-align: center;">{{ item?.cost_date ? moment(item.cost_date).format('YYYY-MM-DD') : '' }}</td>
                                            <td colspan="2" style="text-align: right;">
                                                {{ item?.curr_cost ? '₩ ' + numeral(item.curr_cost).format('0,0') : '' }}
                                            </td>
                                            <td colspan="1" style="text-align: center;">{{ item?.total_cost_rate ? numeral(item.total_cost_rate).format('0.0%') : '' }}</td>
                                        </tr>
                                        <tr style="border: 2px solid #000000;">
                                            <th colspan="2" style="text-align: center;">누계</th>
                                            <th colspan="2" style="text-align: right;">
                                                {{ vars.dataSource.projectOutCostLog && vars.dataSource.projectOutCostLog.length > 0 ? '₩ ' + numeral(vars.dataSource.projectOutCostLog.filter(item => item && item.curr_cost).reduce((acc, item) => acc + (item.curr_cost || 0), 0)).format('0,0') : '₩ 0' }}
                                            </th>
                                            <th colspan="1" style="text-align: center;">
                                                {{ vars.dataSource.projectOutCostLog && vars.dataSource.projectOutCostLog.length > 0 ? numeral(vars.dataSource.projectOutCostLog[vars.dataSource.projectOutCostLog.length - 1].total_cost_rate).format('0.0%') : '0%' }}
                                            </th>
                                        </tr>
                                        <tr class="no-border-row">
                                            <td colspan="5" style="padding-top: 20px; padding-bottom: 20px; padding-left: 10px;">&nbsp;</td>
                                        </tr>
                                        <tr style="border-top: 2pt solid #000000;">
                                            <th colspan="3">{{ vars.dataSource.projectExcutionPlanSubcontract?.subcontract_company || '' }} 잔여기성</th>
                                            <th style="text-align: right;">{{ vars.dataSource.projectOutCostLog && vars.dataSource.projectOutCostLog.length > 0 ? '₩ ' + numeral(vars.dataSource.projectOutCostLog[vars.dataSource.projectOutCostLog.length - 1].remaining_cost).format('0,0') : '₩ 0' }}</th>
                                            <th style="text-align: center;">{{ vars.dataSource.projectOutCostLog && vars.dataSource.projectOutCostLog.length > 0 ? numeral((1 - vars.dataSource.projectOutCostLog[vars.dataSource.projectOutCostLog.length - 1].total_cost_rate) * 100).format('0.0') + '%' : '100%' }}</th>
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
import { projectCostLog, projectOutCostLog, projectRegistration, projectExcutionPlanSubcontract } from '../../data-source/project';
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
        projectId: {
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
            approvalLine2: [],
            approvalStatus: "",
            approvalResult: null,
            projectCostLog: null,
            projectOutCostLog: null,
            projectExcutionPlanSubcontract: null,
        });

        vars.formData = reactive({});
        const signImages = computed(() => {
            if (!vars.dataSource.approvalLine.length && !vars.dataSource.approvalLine2.length) return {};
            
            return [...vars.dataSource.approvalLine, ...vars.dataSource.approvalLine2].reduce((acc, line, index) => {
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
                
                if (props.projectId > 0) {
                    await methods.getApprovalLine();
                    await methods.getApprovalStatus();
                    
                    let { data : projectManagementData } = await projectRegistration.byKey(props.projectId);
              
                    if (projectManagementData) {
                        Object.assign(vars.formData, projectManagementData);

                        let { data : projectExcutionPlanSubcontractData } = await projectExcutionPlanSubcontract.load({ filter: [['fk_project_excution_plan_id', '=', projectManagementData.fk_excution_plan_id]] });

                        if (projectExcutionPlanSubcontractData.length > 0) {
                            vars.dataSource.projectExcutionPlanSubcontract = projectExcutionPlanSubcontractData[0] || null;
                        }
                    }
                    


                    let { data : projectCostLogData } = await projectCostLog.load({ filter: [['fk_project_management_id', '=', props.projectId]], order: [['cost_date', 'desc']] });
                    let { data : projectOutCostLogData } = await projectOutCostLog.load({ filter: [['fk_project_management_id', '=', props.projectId]], order: [['cost_date', 'desc']] });
                    
                    const maxLength = Math.max(
                        projectCostLogData?.length || 0,
                        projectOutCostLogData?.length || 0
                    );
                    
                    if (projectCostLogData && projectCostLogData.length < maxLength) {
                        const emptyItems = Array(maxLength - projectCostLogData.length).fill(null).map(() => ({}));
                        vars.dataSource.projectCostLog = [...projectCostLogData, ...emptyItems];
                    } else {
                        vars.dataSource.projectCostLog = projectCostLogData || [];
                    }
                    
                    if (projectOutCostLogData && projectOutCostLogData.length < maxLength) {
                        const emptyItems = Array(maxLength - projectOutCostLogData.length).fill(null).map(() => ({}));
                        vars.dataSource.projectOutCostLog = [...projectOutCostLogData, ...emptyItems];
                    } else {
                        vars.dataSource.projectOutCostLog = projectOutCostLogData || [];
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
                if (props.projectId > 0) {
                    getApproval([{ name: 'fk_project_id', op: 'eq', val: props.projectId || 0}, { name: 'fk_document_id', op: 'eq', val: 4}]).load().then((response) => {
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
                            ['fk_project_id', '=', props.projectId],
                            ['fk_document_id', '=', 4]
                        ]
                    })
                    if (approvalData.length > 0) {
                        vars.dataSource.approvalLine = approvalData[0].approval_line_result?.filter(item => item.line_type == 1);
                        vars.dataSource.approvalLine2 = approvalData[0].approval_line_result?.filter(item => item.line_type == 2);
              
                    } else {
                        const { data : approvalLineData } = await approvalLine.load({
                            filter: [
                                ['fk_request_emp_id', '=', authService.user?.emp_id || 0],
                                'and',
                                ['fk_document_id', '=', 4]
                            ],
                            sort: [
                                {
                                    selector: 'line_order',
                                    desc: false
                                }
                            ]
                        });
                        if (approvalLineData.length > 0) {
                            console.log(approvalLineData);
                            vars.dataSource.approvalLine = approvalLineData?.filter(item => item.line_type == 1);
                            vars.dataSource.approvalLine2 = approvalLineData?.filter(item => item.line_type == 2);
                        }
                        else {
                            vars.dataSource.approvalLine = [];
                            vars.dataSource.approvalLine2 = [];
                        }
                    }
                    if (vars.dataSource.approvalLine.length == 0 && vars.dataSource.approvalLine2.length == 0) {
                        notifyError('결재선이 존재하지 않습니다. 결재선을 지정해주세요.');
                    }
                }
               
                catch (error) { 
                    console.error('getApprovalLine error:', error);
                }
            },
            async resetData() {
                Object.keys(vars.formData).forEach(key => delete vars.formData[key]);
                // 배열 속성은 빈 배열로 초기화
                vars.dataSource.approvalLine = [];
                vars.dataSource.approvalLine2 = [];
                vars.dataSource.projectCostLog = null;
                vars.dataSource.projectOutCostLog = null;
                vars.dataSource.projectExcutionPlanSubcontract = null;
                vars.dataSource.approvalStatus = "";
                vars.dataSource.approvalResult = null;
            },
            async printReport() {
                vars.loading.value = true;
                await printReport('', [], document.querySelector('.progress-payment-report'), { landscape: true });
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

                if (vars.dataSource.approvalLine.length == 0 || vars.dataSource.approvalLine2.length == 0) {
                    alert('결재선이 존재하지 않습니다. 결재선을 지정해주세요.', '결재선 지정');
                    return;
                }
              
                const result = await confirm('상신하시겠습니까?', '상신');
                if (!result) return;
                
                vars.loading.value = true;

                try {
                    const approvalFormData = {
                        document_name : '기성고검토보고서',
                        fk_project_id: props.projectId,
                        fk_company_id: authService.getCompanyId(),
                        fk_document_id: 4,
                        approval_date: currentDateTime(),
                        approval_status: '상신완료',
                        approval_document: {id: 4},
                        fk_request_emp_id: authService.user?.emp_id,
                    }
                    const { data : approvalData } = await approval.insert(approvalFormData);
                    if (approvalData.id) {  
                        let count = 0;
                        for (const line of vars.dataSource.approvalLine) {

                            const arFormData = {
                                line_header: line.line_header,
                                approval_result: '대기중',
                                line_type: 1,
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
                        count = 0;
                        for (const line of vars.dataSource.approvalLine2) {
                            const arFormData = {
                                line_header: line.line_header,
                                approval_result: '대기중',
                                line_type: 2,
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
            async handleApproval(){
                const resultData = vars.dataSource.approvalResult;
                console.log("resultData : ", resultData);
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
                    approval.load({ filter: [['fk_project_id', '=', props.projectId], ['fk_document_id', '=', 4]] }).then(async (response) => {
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
    
        const currentMonth = computed(() => {
            const month = moment().month() + 1; 
            return '(' + month + ')';
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
            signImages,
            currentMonth,
        };
    },
};
</script>

<style lang="scss">
.progress-payment-report {
    .bg-gray {
        background-color: #e0e0e0;
    }
    .report {
        font-family: '맑은 고딕', 'Malgun Gothic', sans-serif; 
        -webkit-print-color-adjust: exact; 
        width: 297mm; 
        height: 210mm; 
        box-sizing: border-box; 
        padding: 8px;
        font-size: 15px;
        border: 1px dotted #9c9c9c;
        table {width: 100%; border-collapse: collapse; table-layout: fixed;}
        .content-header {
            margin-top: 20px;
            margin-bottom: 20px;
            display: flex;
            width: 100%;
            justify-content: center;
            
    
            .content-header-title {
                font-size: 30px;
                font-weight: bold;
                text-align: center;
            }

        }
        .content-header-approval-line {
            width: 50%;
            display: flex;
            justify-content: right;
            
            .approval-line-table {
                width: auto; 
                border-collapse: collapse;
                border: 2px solid #000;
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
           
        }
        .content-body {
            margin-top: 20px;
            width: 100%;
            .content-area-1 {
                width: 100%;
                table {
                    border: 2px solid #000000;
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 12px;
                    tr {
                        th, td {
                            box-sizing: border-box;
                            border-right: 1pt solid #000000 !important;
                            border-bottom: 1pt solid #000000 !important;
                            padding: 2px;
                            white-space: nowrap;
                        }
                        
                    }
                   
                    tr:first-child th,
                    tr:first-child td {
                        border-top: 1pt solid #000000 !important;
                    }
                    tr th:first-child,
                    tr td:first-child {
                        border-left: 1pt solid #000000 !important;
                    }
                    tr th:last-child,
                    tr td:last-child {
                        border-right: 1pt solid #000000 !important; 
                    }
                    tr:last-child th,
                    tr:last-child td {
                        border-bottom: 1pt solid #000000 !important; 
                    }
                  
                    tr.no-border-row {
                        th, td {
                            border: none !important;
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
                    
                    
                    
                }
            }
            .content-area-2 {
                box-sizing: border-box;
                display: flex; 
                justify-content: space-between; 
                align-items: flex-start;
                width: 100%; 
                margin-top: 20px;
                table {
                    font-size: 12px;
                    border: none;
                    
                }
             
                tr {
                    th, td {
                        height: 25px;
                        box-sizing: border-box;
                        border-right: 1pt solid #000000 !important;
                        border-bottom: 1pt solid #000000 !important;
                        padding: 2px;
                        white-space: nowrap;
                    }
                }
           
                tr:first-child th,
                tr:first-child td {
                    border-top: 2pt solid #000000 !important;
                }
                tr th:first-child,
                tr td:first-child {
                    border-left: 2pt solid #000000 !important;
                }
                tr th:last-child,
                tr td:last-child {
                    border-right: 2pt solid #000000 !important; 
                }
                tr:last-child th,
                tr:last-child td {
                    border-bottom: 2pt solid #000000 !important;
                }
               
                tr.no-border-row {
                    th, td {
                        border: none !important;
                    }
                }
            }
        }
    }
    
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