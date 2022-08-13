from __future__ import print_function
import sys
import os
import json
import copy
import traceback
from collections import OrderedDict

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format('..')))

from commons.jsonproc import JSONProc

class ClusterInfo:
    cluster_file = None
    cluster_info_file = None

    def process_file(self):
        out_data = {}
        try:
            with open(self.cluster_file, 'r') as cluster_list_file:
                cluster_list = json.load(cluster_list_file, object_pairs_hook=OrderedDict)
                for i in range(len(cluster_list)):
                    cluster = cluster_list[i]
                    nodes = []
                    info = {}
                    full_cluster = {}
                    cluster_ip_list = cluster['ipToNodeMap']
                    seed_ip_list = cluster['seeds']
                    for node in cluster_ip_list:
                        if cluster_ip_list[node]['ip'] in seed_ip_list:
                            self.add_node(nodes, cluster_ip_list[node]['ip']+'-'+cluster_ip_list[node]['dc']+'-seed')
                        else:
                            self.add_node(nodes, cluster_ip_list[node]['ip']+'-'+cluster_ip_list[node]['dc']+'-Non_seed')
                    full_cluster['nodes'] = nodes
                    info['DeploymentID'] = int(cluster['deploymentId'])
                    info['SealID'] = int(cluster['sealId'])
                    info['CostCenter'] = int(cluster['costCenter'])
                    info['NodeType'] = cluster['nodeSize']
                    info['Nodes'] = int(len(nodes))
                    info['StorageType'] = cluster['storageType']
                    full_cluster['info'] = info
                    out_data[cluster['id'] + '-' + cluster['name']] = full_cluster
            cluster_list_file.close()
        except:
            print(traceback.format_exc())
            return -1
        try:
            with open(self.cluster_info_file, 'r') as cluster_info_file:
                cluster_info = json.load(cluster_info_file, object_pairs_hook=OrderedDict)
                dev = copy.deepcopy(cluster_info['cassandra']['cqlsh']['connect-parm']['dev-qa'])
                uatv = copy.deepcopy(cluster_info['cassandra']['cqlsh']['connect-parm']['uatv'])
                perf = copy.deepcopy(cluster_info['cassandra']['cqlsh']['connect-parm']['perf'])
                prod = copy.deepcopy(cluster_info['cassandra']['cqlsh']['connect-parm']['prod'])
                dev['clusters'] = {}
                uatv['clusters'] = {}
                perf['clusters'] = {}
                prod['clusters'] = {}
                got_in_json = ''
                for key in out_data:
                    if 'DEV' in key.upper() or 'QA' in key.upper() or 'JANGO' in key.upper():
                        dev['clusters'][key] = out_data[key]
                        if '-DEV-' not in got_in_json:
                            got_in_json = got_in_json + '-DEV-'
                    elif 'UAT' in key.upper():
                        dev['clusters'][key] = out_data[key]
                        if '-UATV-' not in got_in_json:
                            got_in_json = got_in_json + '-UATV-'
                    elif 'PERF' in key.upper():
                        dev['clusters'][key] = out_data[key]
                        if '-PERF-' not in got_in_json:
                            got_in_json = got_in_json + '-PERF-'
                    elif 'PROD' in key.upper():
                        dev['clusters'][key] = out_data[key]
                        if '-PROD-' not in got_in_json:
                            got_in_json = got_in_json + '-PROD-'
                connect_parm = cluster_info['cassandra']['cqlsh']['connect-parm']
                if '-DEV-' in got_in_json:
                    connect_parm['dev-qa']['clusters'] = dev['clusters']
                if '-UATV-' in got_in_json:
                    connect_parm['uatv']['clusters'] = uatv['clusters']
                if '-PERF-' in got_in_json:
                    connect_parm['perf']['clusters'] = perf['clusters']
                if '-PROD-' in got_in_json:
                    connect_parm['prod']['clusters'] = prod['clusters']
                cluster_info_file.close()
        except:
            return -1
        try:
            with open(self.cluster_info_file, 'w') as connect_file:
                connect_file.write(json.dumps(cluster_info, indent=2))
                connect_file.close()
                return 0
        except:
            return -1

    def add_node(self, nodes, node_info):
        if node_info not in nodes:
            nodes.append(node_info)
        return nodes

    def __init__(self, in_file, out_file):
        self.cluster_file = in_file
        self.cluster_info_file = out_file
        return
    
if __name__ == '__main__':
    cluster_info = ClusterInfo('..\\conf\\clusterinfo.json', '..\\conf\\connect.json')
    cluster_info.process_file()