<script setup>
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxButtonItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form'
import { DxButton } from 'devextreme-vue/button'
import { ref, watch, computed, defineProps, defineEmits, onMounted } from 'vue'
import { DxLoadPanel } from 'devextreme-vue/load-panel'
import moment from 'moment'
import { baseClient } from '@/data-source/base'
import ApiService from '@/utils/api-service'
import authService from '@/auth'
import { notifyInfo, notifyError } from '@/utils/notify'

const BAROBILL_STATE = {
    1000 : '임시저장',
    2010 : '발급예정 승인대기',
    2011 : '발급예정 승인완료',
    2020 : '역발행요청 발급대기',
    3011 : '발급예정 발급완료',
    3021 : '역발행요청 발급완료',
    3014 : '발급완료',
    4012 : '발급예정 거부',
    4022 : '역발행요청 거부',
    5013 : '발급예정 승인 전 공급자에 의한 취소',
    5023 : '역발행요청 승인 전 공급받는자에 의한 취소',
    5031 : '발급예정 승인 후, 또는 발급완료 후 공급자에 의한 취소'
}

const NTS_SEND_STATE = {
    1 : '전송전',
    2 : '전송대기',
    3 : '전송중',
    4 : '전송완료',
    5 : '전송실패'
}

const props = defineProps({show: Boolean, number: String, formData: Object, items: Array})
const emit = defineEmits(['close'])
const loading = ref(false)
const customerInfo = ref({
    address: '',
	address_detail: '',
	address_en: '',
	after_alias: '',
	alias: '',
	before_alias: '',
	bill_email: '',
	bill_manager: '',
	business_number: '',
    business_name: '',
	business_sector: '',
	business_status: '',
	ceo_name: '',
	ceo_name_en: '',
	client_type: '',
	corp_number: '',
	created: '',
	district_type: '',
	email: '',
	etc: null,
	fax: '',
	fax_en: '',
	fk_company_id: 1,
	homepage: '',
	id: 0,
	last_updated_date: '',
	manager: '',
	modify_id: '',
	name: '',
	name_en: '',
	phone: '',
	phone_en: '',
	register_id: '',
	trade_yn: false,
	zip_code: ''
})
const apiService = new ApiService('/api/mes/v1/barobill')
const companyId = authService.getCompanyId()

console.log(authService.user)

const formData = ref({
    ...props.formData,
    stateString: '',
    stateCode: -21002,
    processDetail: ''
})

// 등록/발급 가능 상태: 기존 문서가 없는 경우
const disableIssue = computed(() => ![-21002].includes(formData.value.stateCode))
// 취소 가능 상태:
const disableCancel = computed(() => ![1000, 2010, 2011, 2020, 3011, 3021, 3014].includes(formData.value.stateCode))
// 수정 가능 상태: ???
const disableUpdate = computed(() => ![1000, 2010, 2011, 2020, 3011, 3021, 3014].includes(formData.value.stateCode))
// 삭제 가능 상태: 임시저장, 취소, 거부
const disableDelete = computed(() => ![1000, 4012, 4022, 5013, 5023, 5031].includes(formData.value.stateCode))

onMounted(initialize)

watch(
    () => props.show,
    () => updateState()
)

async function initialize () {
    console.info('세금계산서 뷰 마운트 됨')
    await updateState()
}

async function getClientInfoByName (name) {
    console.info(`고객사 정보 업데이트: ${name}`)
    const {data: list} = await baseClient.load({
        filter: [
            ['name', '=', name], 
            'and', 
            ['fk_company_id', '=', companyId]
        ]
    })
    if (list.length) {
        Object.assign(customerInfo.value, list[0])
    }
    else {
        formData.value.processDetail = '고객사 정보가 없습니다'
        console.error('고객사 정보가 없습니다')
    }
}

async function updateState () {
    console.info('세금계산서 상태 업데이트')
    for (const key of Object.keys(props.formData)) {
        formData.value[key] = props.formData[key]
    }
    formData.value.processDetail = ''
    await getClientInfoByName(formData.value.client_company)
    console.log(customerInfo.value)

    
    loading.value = true
    const {data: state} = await apiService.get(`state/${props.number}`)
    formData.value.stateCode = state.data.BarobillState

    if (state.success === false) formData.value.stateString = state.error_message
    else {
        formData.value.stateString = BAROBILL_STATE[formData.value.stateCode]
        formData.value.processDetail = 
            `국세청 전송상태: ${NTS_SEND_STATE[state.data.NTSSendState]}\n`
          + `국세청 승인번호: ${state.data.NTSSendKey}`
    }
    loading.value = false
}

function calcPriceSummary (vat_type, total) {
  let supply_price = 0;
  let vat = 0;
  let total_price = 0;

  switch (vat_type) {
    case '별도': {
      supply_price = total;
      vat = Math.floor(total * 0.1) - (props.formData.vat_adjustment || 0);
      total_price = total + vat;
      break;
    }
    case '포함': {
      total_price = total;
      supply_price = Math.round((total * 10) / 11) - (props.formData.vat_adjustment || 0);
      vat = total_price - supply_price;
      break;
    }
    case '영세': {
      total_price = total;
      vat = 0;
      supply_price = total;
      break;
    }
    default: {
      total_price = total;
      vat = 0;
      supply_price = total;
    }
  }
  return { supply_price, vat, total_price }
}

async function registerInvoice () {
    console.info('세금계산서 등록 및 발행')
    if (!props.items.length) {
        notifyError('품목이 없습니다')
        return console.error('품목 없음')
    }
    if (!customerInfo.value.business_number) {
        notifyError('고객사 정보가 없습니다')
        return console.error('고객사 정보가 없습니다')
    }
    loading.value = true
    const {data: company} = await getCompanyInfo()
    const total = props.items.reduce((t, a) => {
        t += Number(a.supply_price)
        return t
    }, 0)

    const summary = calcPriceSummary(props.formData.vat_type, total)
    const currentDate = moment(props.formData.sales_date).format('YYYYMMDD')

    const items = [{
        PurchaseExpiry: currentDate,
        Name: props.items[0].statement_item + (props.items.length === 1 ? '' : ' 외'),
        Information: '',
        ChargeableUnit: '',
        UnitPrice: '',
        Amount: String(summary.supply_price),
        Tax: String(summary.vat),
        Description: '',
    }]
    const params = {
        InvoicerParty: {
            MgtNum: props.number,
            CorpNum: company.business_number.replace(/\D/g, ''),
            CorpName: company.name,
            CEOName: company.ceo_name,
            Addr: company.address,
            ContactID: 'stechinc',
            ContactName: company.bill_manager,
            TEL: company.phone,
            HP: '',
            Email: company.bill_email,
            BizClass: company.business_sector,
            BizType: company.business_status
        },
        InvoiceeParty: {
            CorpNum: customerInfo.value.business_number,
            CorpName: customerInfo.value.business_name,
            CEOName: customerInfo.value.ceo_name,
            Addr: customerInfo.value.address,
            ContactName: customerInfo.value.bill_manager,
            TEL: customerInfo.value.phone,
            Email: customerInfo.value.bill_email,
            BizClass: customerInfo.value.business_sector,
            BizType: customerInfo.value.business_status
        },
        // TaxInvoiceTradeLineItems: props.items.map(item => ({
        //     PurchaseExpiry: currentDate,
        //     Name: item.item.item_name,
        //     Information: item.item.item_standard,
        //     ChargeableUnit: String(item.quantity),
        //     UnitPrice: String(item.unit_price),
        //     Amount: String(item.supply_price),
        //     Tax: String(item.vat),
        //     Description: '',
        // })),
        WriteDate: currentDate,
        TaxInvoiceTradeLineItems: items,
        PurposeType: props.formData.approval_type === '청구' ? 2 : 1, // 1 : 영수,  2 : 청구
        AmountTotal: String(summary.supply_price),
        TaxTotal: String(summary.vat),
        TotalAmount: String(summary.total_price),
        Remark1: props.formData.etc,
    }
    console.log(params)

    const {data: result} = await apiService.post('invoice', params)
    if (result.success) {
        notifyInfo('계산서가 등록 및 발행되었습니다.')
        await updateState()
    }
    else {
        notifyError(result.error_message)
        loading.value = false
    }
}

async function cancelInvoice () {
    console.info('세금계산서 취소')
    loading.value = true

    const procType = 'ISSUE_CANCEL'
    const params = { memo: '' }
    const {data: result} = await apiService.patch(`state/${props.number}/${procType}`, params)
    
    if (result.success) {
        notifyInfo('계산서가 취소되었습니다.')
        await updateState()
    }
    else {
        notifyError(result.error_message)
        loading.value = false
    }
}

async function deleteInvoice () {
    console.info('세금계산서 삭제')
    loading.value = true
    const {data: result} = await apiService.delete(`state/${formData.value.sales_number}`)

    if (result.success) {
        notifyInfo('계산서가 삭제되었습니다.')
        await updateState()
    }
    else {
        notifyError(result.error_message)
        loading.value = false
    }
}

async function previewPopup () {
    console.info('세금계산서 미리보기')
    loading.value = true
    const params = {
        MgtNum: props.number,
        ContactID: 'stechinc'
    }
    const {data: result} = await apiService.post('popup/invoice', params)
    if (result.success) window.open(result.data, 'barobill', 'width=870,height=800')
    loading.value = false
}

async function getCompanyInfo () {
    const apiService = new ApiService('/api/mes/v1/common')
    return await apiService.get(`companies/${companyId}`)
}

function closeDialog () {
    emit('close')
}
</script>

<template>
    <dx-button class="close-btn" icon="close" styling-mode="text" @click="closeDialog()"></dx-button>
    <dx-load-panel v-model:visible="loading" :show-pane="true" />
    <dx-form :form-data="formData"
        :show-colon-after-label="false">
        <dx-group-item caption="세금계산서 정보" :col-count="5">
            <dx-group-item :col-span="2">
                <dx-simple-item data-field="sales_number" :label="{text: '계산서번호'}" :editor-options="{readOnly: true}" />
                <dx-simple-item data-field="sales_number" :label="{text: '전송 연결번호'}" :editor-options="{readOnly: true}" />
                <dx-simple-item data-field="stateString" css-class="barobill-state" :label="{text: '현재상태'}" :editor-options="{readOnly: true}" />
                <dx-simple-item data-field="stateCode" :label="{text: '결과코드'}" :editor-options="{readOnly: true}" />
            </dx-group-item>
            <dx-simple-item template="bill-func" :col-span="3" />
            <dx-simple-item :col-span="5" data-field="processDetail" editor-type="dxTextArea" :label="{text: '처리내용'}" :editor-options="{readOnly: true}" />
        </dx-group-item>
        
        <template #bill-func>
            <table class="bill-func-table">
                <colgroup>
                    <col class="bill-col" />
                    <col class="bill-col" />
                    <col class="bill-col" />
                </colgroup>
                <tr>
                    <td><dx-button class="bill-func-btn" type="success" :disabled="disableIssue" @click="registerInvoice()">즉시발행</dx-button></td>
                    <td><dx-button class="bill-func-btn" :disabled="disableCancel" @click="cancelInvoice()">취소요청</dx-button></td>
                    <td><dx-button class="bill-func-btn" type="default" @click="updateState()">상태확인</dx-button></td>
                </tr>
                <tr>
                    <td><dx-button class="bill-func-btn" :disabled="disableUpdate">계산서 수정</dx-button></td>
                    <td><dx-button class="bill-func-btn" type="danger" :disabled="disableDelete" @click="deleteInvoice()">계산서 삭제</dx-button></td>
                    <td><dx-button class="bill-func-btn" :disabled="disableUpdate">E-mail 재전송</dx-button></td>
                </tr>
                <tr>
                    <td colspan="3"><dx-button class="bill-func-btn" type="success" :disabled="disableCancel" @click="previewPopup()">전자 세금계산서 미리보기</dx-button></td>
                </tr>
            </table>
        </template>
    </dx-form>
    <dx-form :form-data="customerInfo"
        :show-colon-after-label="false">
        <dx-group-item caption="고객사 정보" :col-count="7">
            <dx-simple-item :col-span="2" data-field="business_number" :label="{text: '사업자번호'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="2" data-field="ceo_name" :label="{text: '대표자명'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="3" data-field="alias" :label="{text: '업체코드'}" :editor-options="{readOnly: true}" />

            <dx-simple-item :col-span="2" data-field="phone" :label="{text: '전화번호'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="2" data-field="fax" :label="{text: '팩스번호'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="3" data-field="business_name" :label="{text: '정식상호명'}" :editor-options="{readOnly: true}" />

            <dx-simple-item :col-span="3" data-field="bill_manager" :label="{text: '계산서 담당자'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="4" data-field="bill_email" :label="{text: '계산서 이메일'}" :editor-options="{readOnly: true}" />

            <dx-simple-item :col-span="2" data-field="zip_code" :label="{text: '우편번호'}" :editor-options="{readOnly: true}" />
            <dx-simple-item :col-span="5" data-field="address" :label="{text: '주소'}" :editor-options="{readOnly: true}" />
        </dx-group-item>
    </dx-form>
</template>

<style lang="scss" scoped>
:deep(.barobill-state .dx-textbox) {
    box-shadow: inset 0px 1px 3px 0px #38530d6b;
    background-color: #e3ffb8;
    color: #5c8816;
}
.bill-func-table {
    table-layout: fixed;
    width: 100%; height: 160px;
    min-width: 216px;
    td {
        padding: 6px;
    }
}
.bill-func-btn {
    width: 100%; height: 100%;
}
.bill-col {
    width: 33.3%;
}

.close-btn {
    position: absolute;
    top: 14px; right: 2px;
}
</style>