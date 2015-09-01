# coding:utf:8
__author__ = 'kevin yuan'
import requests

class SaltStack(object):

    cookies = None
    host = None

    def __init__(self, host, username, password, port='8000', secure=True, eproto='pam'):
        proto = 'https' if secure else 'http'
        self.host = '%s://%s:%s' % (proto, host, port)

        self.login_url = self.host + "/login"
        self.logout_url = self.host + "/logout"
        self.minions_url = self.host + "/minions"
        self.jobs_url = self.host + "/jobs"
        self.run_url = self.host + "/run"
        self.events_url = self.host + "/events"
        self.ws_url = self.host + "/ws"
        self.hook_url = self.host + "/hook"
        self.stats_url = self.host + "/stats"

        r = requests.post(self.login_url, verify=False, data={'username': username,
                                                          'password': password,
                                                          'eauth': eproto})

        if r.status_code == 200:
            self.cookies = r.cookies
        else:
            raise Exception('Error from source %s' % r.text)

    def cmd_run(self, tgt, commond, expr_form='compound', fun='cmd.run'):
        r = requests.post(self.host, verify=False, cookies=self.cookies, data={'tgt': tgt, 
                                                                                'client': 'local',
                                                                                'expr_form': expr_form, 
                                                                                'fun': fun, 
                                                                                'arg': commond})
        if r.status_code == 200:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)
 
    def manage_status(self):
        r = requests.post(self.host, cookies=self.cookies, data={'client': 'runner',
                                                                'fun': 'manage.status'})
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Error from source %s' % r.text)
            

    def job_info(self, jid="None"):
        try:
            job_url = self.jobs_url + '/' + jid
        except:
            raise Exception('jid error')
        r = requests.get(job_url, verify=False, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['info'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def job_result(self, jid="None"):
        try:
            job_url = self.jobs_url + '/' + jid
        except:
            raise Exception('jid error')
        r = requests.get(job_url, verify=False, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def cp_file(self, tgt, from_path, to_path, expr_form='compound'):
        r = requests.post(self.host, verify=False, cookies=self.cookies, data={'tgt': tgt,
                                                                                'client': 'local',
                                                                                'fun': 'cp.get_file',
                                                                                'arg': [from_path, to_path],
                                                                      })
        if r.status_code == 200:
            print type(r.json())
            return r.json()
        else:
            raise Exception('Error from source %s' % r.text)
 
    def get_minion_detail(self, tgt="*", expr_form='compound', client='runner'):
        r = requests.post(self.minions_url, verify=False, data={'tgt': tgt,
                                                  'fun': "status.diskusage"}, cookies=self.cookies)

        if r.status_code == 202:
            return r.json()['return'][0]
        else:
            raise Exception('Error from source %s' % r.text)

    def get_disk_usage(self, tgt, expr_form='compound'):
        pass

    def get_ip_addr(self, tgt, expr_form='compound', client='local'):
        r = requests.post(self.host, verify=False, data={'fun': 'network.interface_ip',
                                             'tgt': tgt,
                                             'client': client,
                                             'expr_form': expr_form,
                                             'arg': 'eth0'}, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)

    def restart_service(self, tgt, service, expr_form='compound', client='local'):
        """

        :param tgt: target
        :param service: service name
        :param expr_form:
        :param client:
        :return: :raise Exception:
        """
        r = requests.post(self.host, verify=False, data={'fun': 'service.restart',
                                             'tgt': tgt,
                                             'client': client,
                                             'expr_form': expr_form,
                                             'arg': service}, cookies=self.cookies)

        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)

    def get_roles(self, tgt, expr_form='compound', client='local'):
        """

        :param tgt: target
        :param expr_form: match style
        :param client: local/runner/wheel
        :return: :raise Exception: api error
        """
        r = requests.post(self.host, data={'fun': 'grains.item',
                                             'tgt': tgt,
                                             'client': client,
                                             'expr_form': expr_form,
                                             'arg': 'ipv4'}, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()['return']
        else:
            raise Exception('Error from source %s' % r.text)


def demo():
    print HOST, PORT, USER, PASS, SECURE
    sapi = SaltStack(host=HOST,
                 port=PORT,
                 username=USER,
                 password=PASS,
                 secure=SECURE)
    print sapi.host
    print sapi.cookies
    # print sapi.get_minion_detail('*')
    # print sapi.job_info(jid='20150824220447986810')
    # print sapi.job_result(jid='20150824220447986810')
    # from_path = "salt://share/SIS-PA18-DEPLOY/SIS-PA186.19.0/SIS-PA186.19.0.4/app/openwebapp/6.18.0.xls"
    # to_path = "/root/6.18.0.xls"
    # print sapi.cp_file('10.25.27.114', from_path=from_path, to_path=to_path)
    # print sapi.cmd_run('10.25.153.173', '/bin/sh /wls/wls81/test.sh')
    print sapi.manage_status()
    # print sapi.
    # print sapi.get_ip_addr('10.25.27.114')
    # print sapi.get_ip_addr('*')
    # print sapi.minions_url
    # print sapi.cookies
    # print sapi.get_ip_addr("*", client='local')[0]
    # print sapi.get_minion_details()
    # dict =  sapi.get_roles('*')[0]
    # print dict
    # for minion, result in dict.items():
    #     print minion, result


if __name__ == "__main__":
    from placeholders import *
    demo()