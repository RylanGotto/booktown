import logging
from suds.client import Client
from suds.wsse import *
from idmlib.agent import Agent
from suds.plugin import MessagePlugin
from suds.sax import document
import urllib.request as Req
import xml.etree.ElementTree as ET
import re

from base64 import b64encode
#from idmlib import win32
#from idmlib.common import Config
#from idmlib.globals import API

wsdl_url = 'https://wd5-services1.myworkday.com/ccx/service/talisman/Human_Resources?wsdl'
list_url = 'https://wd5-services1.myworkday.com/ccx/service/customreport2/talisman/TLIISU_Report_Owner/TLI1004CR_PM_User'

proxy_settings = dict(http='passwman_svc:Te#&ick83mas@calproxy.na.tlm.com:8080',
                      https='passwman_svc:Te#&ick83mas@calproxy.na.tlm.com:8080')


class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        id_object = context.envelope.getChild('Body')\
            .getChild('Workday_Account_for_Worker_Update')\
            .getChild('Worker_Reference')\
            .getChildren()[0]\
            .getChild('Integration_ID_Reference')\
            .getChild('ID')\
            .getAttribute('System_ID')

        prefixes = context.envelope.nsprefixes
        for key, value in prefixes.items():
            if value == 'urn:com.workday/bsvc':
                id_object.prefix = key


class WorkdayTarget(Agent):

    def connect(self):
        return self.ACSuccess

    # Only really used for testing connectivity, might be worth implementing later on
    def serverinfo(self):
        return self.ACSuccess

    # Users are listed as username + "|||" + employee_id + "|||" + worker_type
    # because attributes can't be passed into a reset operation
    def list(self):
        user_xml = read_user_list(self.adminid, self.adminpw)
        users = ET.fromstring(user_xml)
        for user in users:

            username = user.find('{urn:com.workday.report/TLI1004CR_PM_User}User_Name').text.upper()
            employee_id = user.find('{urn:com.workday.report/TLI1004CR_PM_User}Employee_ID').text
            worker_type = user.find('{urn:com.workday.report/TLI1004CR_PM_User}TLI1003CF_Worker_Type').text.upper()
            listname = username + '|||' + employee_id + "|||" + worker_type
            attrs = {'listname': listname, 'workday_name': username, 'employeeID': employee_id, 'worker_type': worker_type}
            agent.agentListUser(listname, listname, listname, attrs)

        return self.ACSuccess

    def reset(self):
        return account_update(self)

    def verifyreset(self):
        return self.reset()

    def change(self):
        return account_update(self, reenable=True)

    # These operations aren't being used but are partially implemented
    def enable(self):
        account_update(self, unlock=True)

    def disable(self):
        account_update(self, unlock=False)

    # Verifying against workday may be possible, but does not make sense for Talisman
    def adminverify(self):
        return self.ACOperationNotSupported

    def verify(self):
        return self.ACOperationNotSupported

    # Workday doesn't expire passwords, so these operations are unnecessary
    def resetexpirepw(self):
        return self.reset()

    def expirepw(self):
        return self.ACOperationNotSupported

    def unexpirepw(self):
        return self.ACOperationNotSupported

    def ispwexpired(self):
        self.agentIsPassExpired(False)
        return self.ACSuccess

    def disconnect(self):
        return self.ACSuccess


# Update user information using the SOAP API
def account_update(self, reenable=False, unlock=None):
    user_ids = self.acctid.split('|||')
    username = user_ids[0]
    employee_id = user_ids[1]
    worker_type = user_ids[2]
    print(username, employee_id, worker_type)
    client = create_client()
    worker_ref = generate_worker_ref(client, employee_id, worker_type)

    if unlock is not None:
        wafwd = generate_wafwd(client, username, disabled=unlock)
    elif reenable:
        wafwd = generate_wafwd(client, username, password=self.acctpw, disabled=False)
    else:
        wafwd = generate_wafwd(client, username, password=self.acctpw)

    security = generate_security(self.adminid, self.adminpw)

    client.set_options(wsse=security)

    try:
        client.service.Update_Workday_Account(worker_ref, wafwd)
    except WebFault as e:

        match = re.search(r"<faultstring>(.*)<\/faultstring>", document.Document.plain(e.document))

        is_invalid = re.findall(r"The password does not meet password requirements", match.group(1))
        if len(is_invalid) > 0:
            self.agentError("The password does not meet password requirements")
            return self.ACInvalidPasswd

        self.agentError("Reset attempt returned the result: " + match.group(1))
        return self.ACUnknownError

    return self.ACSuccess


# List users using the REST API
def read_user_list(username, password):

    username = username.split('@')[0]
    proxy = Req.ProxyHandler(proxy_settings)
    auth = Req.HTTPBasicAuthHandler()
    opener = Req.build_opener(proxy, auth, Req.HTTPHandler)
    Req.install_opener(opener)
    headers = {'Authorization': b'Basic ' +
               b64encode((username + ':' + password).encode('utf-8'))}
    conn = Req.urlopen(Req.Request(list_url, None, headers))
    return conn.read()


# Next three methods just generate the XML
def generate_worker_ref(client, employee_id, worker_type):
    client_id = client.factory.create('ns0:IDType')
    client_id.value = employee_id
    client_id._System_ID = 'WD-EMPLID'

    eiird = client.factory.create('ns0:External_Integration_ID_Reference_DataType')
    eiird.ID = client_id
    
    if worker_type == "EMP":
        employee_ref = client.factory.create('ns0:Employee_ReferenceType')
        print("EMP")
    else:
        employee_ref = client.factory.create('ns0:Contingent_Worker_Reference_DataType')
        print("CWR")
    
    employee_ref.Integration_ID_Reference = eiird

    worker_ref = client.factory.create('ns0:Worker_ReferenceType')
    
    if worker_type == "EMP":
        worker_ref.Employee_Reference = employee_ref
    else:
        worker_ref.Contingent_Worker_Reference = employee_ref

    return worker_ref


def generate_wafwd(client, username, password=None, expire_pw=None, disabled=None):
    wafwd = client.factory.create('ns0:Workday_Account_for_Worker_DataType')
    wafwd.User_Name = username

    if password is not None:
        wafwd.Password = password
    if expire_pw is not None:
        wafwd.Require_New_Password_at_Next_Sign_In = expire_pw
    if disabled is not None:
        wafwd.Account_Disabled = disabled

    return wafwd


def generate_security(username, password):
    security = Security()
    token = UsernameToken(username, password)
    security.tokens.append(token)
    return security


def create_client():
    return Client(wsdl_url, proxy=proxy_settings, plugins=[MyPlugin()])

try:
    agent = WorkdayTarget(log_kvg=True)
    agent.run_agent()
except Exception as error:
    logging.exception(error)
    print(error)

