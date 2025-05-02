from zeep import Client
from backend import app

client = Client(app.config['BAROBILL_API_URL'])
cert_key = app.config['BAROBILL_CERTKEY']
contact_id = app.config['BAROBILL_MNGR_ID']
contact_name = app.config['BAROBILL_MNGR_NAME']
self_corp_num = '3058150966'


def check_member(check_corp_num):
    return client.service.CheckCorpIsMember(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        CheckCorpNum=check_corp_num
    )


def get_invoice_popup_url(mgt_key, pid):
    return client.service.GetTaxInvoicePopUpURL(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKey=mgt_key,
        ID=pid
    )


def issue_invoice(mgt_key):
    return client.service.IssueTaxInvoice(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKey=mgt_key,
        SendSMS=True,
        NTSSendOption=1,
        ForceIssue=False,
        MailTitle='issue test'
    )


# 발급취소
def proc_invoice(mgt_key, proc_type, memo):
    return client.service.ProcTaxInvoice(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKey=mgt_key,
        ProcType=proc_type,
        Memo=memo
    )


def delete_invoice(mgt_key):
    return client.service.DeleteTaxInvoice(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKey=mgt_key
    )


def get_invoice(mgt_key):
    return client.service.GetTaxInvoice(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKey=mgt_key
    )


def get_error_string(err_code):
    return client.service.GetErrString(
        CERTKEY=cert_key,
        ErrCode=err_code
    )


def get_invoice_state(mgt_key):
    return client.service.GetTaxInvoiceStates(
        CERTKEY=cert_key,
        CorpNum=self_corp_num,
        MgtKeyList=client.get_type("ns0:ArrayOfString")([mgt_key])
    )


class InvoiceParty(object):
    def __init__(self):
        self.MgtNum = ''
        self.CorpNum = ''
        self.TaxRegID = ''
        self.CorpName = ''
        self.CEOName = ''
        self.Addr = ''
        self.BizClass = ''
        self.BizType = ''
        self.ContactID = ''
        self.ContactName = ''
        self.TEL = ''
        self.HP = ''
        self.Email = ''

    def to_param(self):
        return client.get_type('ns0:InvoiceParty')(
            MgtNum=self.MgtNum,
            CorpNum=self.CorpNum,
            TaxRegID=self.TaxRegID,
            CorpName=self.CorpName,
            CEOName=self.CEOName,
            Addr=self.Addr,
            BizClass=self.BizClass,
            BizType=self.BizType,
            ContactID=self.ContactID,
            ContactName=self.ContactName,
            TEL=self.TEL,
            HP=self.HP,
            Email=self.Email
        )


class InvoiceTradeLineItem(object):
    def __init__(self):
        self.PurchaseExpiry = ''
        self.Name = ''
        self.Information = ''
        self.ChargeableUnit = ''
        self.UnitPrice = ''
        self.Amount = ''
        self.Tax = ''
        self.Description = ''

    def to_param(self):
        return client.get_type('ns0:TaxInvoiceTradeLineItem')(
            PurchaseExpiry=self.PurchaseExpiry,
            Name=self.Name,
            Information=self.Information,
            ChargeableUnit=self.ChargeableUnit,
            UnitPrice=self.UnitPrice,
            Amount=self.Amount,
            Tax=self.Tax,
            Description=self.Description
        )


class Invoice(object):

    def __init__(self):
        self.InvoicerParty = InvoiceParty()
        self.InvoiceeParty = InvoiceParty()
        self.BrokerParty = InvoiceParty()

        self.InvoicerParty.ContactID = contact_id
        self.InvoicerParty.ContactName = contact_name

        self.InvoiceeASPEmail = ''
        self.IssueDirection = 1
        self.TaxInvoiceType = 1
        self.TaxType = 1
        self.TaxCalcType = 1
        self.PurposeType = 1
        self.ModifyCode = ''
        self.WriteDate = ''
        self.AmountTotal = ''
        self.TaxTotal = ''
        self.TotalAmount = ''
        self.Cash = ''
        self.ChkBill = ''
        self.Note = ''
        self.Credit = ''
        self.Kwon = ''
        self.Ho = ''
        self.SerialNum = ''
        self.Remark1 = ''
        self.Remark2 = ''
        self.Remark3 = ''
        self.TaxInvoiceTradeLineItems = []

    def set_items(self, data):
        item = InvoiceTradeLineItem()
        item.PurchaseExpiry = data['PurchaseExpiry']
        item.Name = data['Name']
        item.Information = data['Information']
        item.ChargeableUnit = data['ChargeableUnit']
        item.UnitPrice = data['UnitPrice']
        item.Amount = data['Amount']
        item.Tax = data['Tax']
        item.Description = data['Description']
        self.TaxInvoiceTradeLineItems.append(item)
        # TODO: calculate

    def items_to_param(self):
        return client.get_type('ns0:ArrayOfTaxInvoiceTradeLineItem')([item.to_param() for item in self.TaxInvoiceTradeLineItems])

    def get_tax_invoice(self):
        return client.get_type('ns0:TaxInvoice')(
            InvoicerParty=self.InvoicerParty.to_param(),
            InvoiceeParty=self.InvoiceeParty.to_param(),
            BrokerParty=self.BrokerParty.to_param(),
            InvoiceeASPEmail=self.InvoiceeASPEmail,
            IssueDirection=self.IssueDirection,
            TaxInvoiceType=self.TaxInvoiceType,
            TaxType=self.TaxType,
            TaxCalcType=self.TaxCalcType,
            PurposeType=self.PurposeType,
            ModifyCode=self.ModifyCode,
            WriteDate=self.WriteDate,
            AmountTotal=self.AmountTotal,
            TaxTotal=self.TaxTotal,
            TotalAmount=self.TotalAmount,
            Cash=self.Cash,
            ChkBill=self.ChkBill,
            Note=self.Note,
            Credit=self.Credit,
            Kwon=self.Kwon,
            Ho=self.Ho,
            SerialNum=self.SerialNum,
            Remark1=self.Remark1,
            Remark2=self.Remark2,
            Remark3=self.Remark3,
            TaxInvoiceTradeLineItems=self.items_to_param()
        )

    def register(self):
        invoice = self.get_tax_invoice()
        return client.service.RegistTaxInvoice(
            CERTKEY=cert_key,
            CorpNum=invoice.InvoicerParty.CorpNum,
            Invoice=invoice
        )

    def register_and_issue(self):
        invoice = self.get_tax_invoice()
        return client.service.RegistAndIssueTaxInvoice(
            CERTKEY=cert_key,
            CorpNum=invoice.InvoicerParty.CorpNum,
            Invoice=invoice,
            SendSMS=True,
            ForceIssue=False,
            MailTitle='test invoice'
        )
